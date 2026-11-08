#!/usr/bin/env python3
"""Weekly Google Search Console report for dogfriendlydg.co.uk.

Reads the GSC bulk export in BigQuery (read-only) and prints a Markdown
report that the weekly SEO agent uses to choose site changes.

Credentials (first match wins):
  GCP_SA_KEY_JSON                 raw service-account JSON (cloud routine)
  GOOGLE_APPLICATION_CREDENTIALS  path to a key file (local use)

Usage:
  pip install google-cloud-bigquery
  python scripts/gsc_report.py [--days 28] > report.md
"""
import argparse
import json
import os
import sys

from google.cloud import bigquery
from google.oauth2 import service_account

PROJECT = "nash-claude-gcp"
DATASET = f"{PROJECT}.searchconsole_dogfriendlydg"
SITE = "https://dogfriendlydg.co.uk"


def client():
    raw = os.environ.get("GCP_SA_KEY_JSON")
    if raw:
        info = json.loads(raw)
        creds = service_account.Credentials.from_service_account_info(info)
        return bigquery.Client(project=PROJECT, credentials=creds)
    if os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        return bigquery.Client(project=PROJECT)
    sys.exit("No credentials: set GCP_SA_KEY_JSON or GOOGLE_APPLICATION_CREDENTIALS")


def table(bq, title, sql, params):
    job = bq.query(sql, job_config=bigquery.QueryJobConfig(query_parameters=params))
    rows = list(job.result())
    print(f"\n## {title}\n")
    if not rows:
        print("_No rows._")
        return
    cols = list(rows[0].keys())
    print("| " + " | ".join(cols) + " |")
    print("|" + "---|" * len(cols))
    for r in rows:
        print("| " + " | ".join("" if r[c] is None else str(r[c]) for c in cols) + " |")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=28, help="current window length")
    days = ap.parse_args().days
    bq = client()

    u = f"`{DATASET}.searchdata_url_impression`"
    s = f"`{DATASET}.searchdata_site_impression`"
    page = f"REGEXP_REPLACE(url, r'^https?://dogfriendlydg\\.co\\.uk', '')"
    # Current window = last N days of available data; previous = the N days before.
    win = f"""
      WITH bounds AS (SELECT MAX(data_date) AS mx FROM {u}),
      w AS (SELECT DATE_SUB(mx, INTERVAL @days - 1 DAY) AS cur_start, mx AS cur_end,
                   DATE_SUB(mx, INTERVAL 2 * @days - 1 DAY) AS prev_start,
                   DATE_SUB(mx, INTERVAL @days DAY) AS prev_end FROM bounds)
    """
    p = [bigquery.ScalarQueryParameter("days", "INT64", days)]

    print(f"# GSC report — last {days} days vs previous {days} days\n")
    print(f"Source: `{DATASET}`. Position = impression-weighted average (1 = top).")

    table(bq, "Data coverage", f"""
      SELECT MIN(data_date) first_day, MAX(data_date) last_day,
             COUNT(DISTINCT data_date) days FROM {u}""", [])

    table(bq, "Weekly totals", f"""
      SELECT DATE_TRUNC(data_date, WEEK(MONDAY)) week, COUNT(DISTINCT data_date) days,
             SUM(clicks) clicks, SUM(impressions) impressions,
             ROUND(SAFE_DIVIDE(SUM(clicks), SUM(impressions)) * 100, 2) ctr_pct,
             ROUND(SUM(sum_position) / SUM(impressions) + 1, 1) position
      FROM {u} WHERE data_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 12 WEEK)
      GROUP BY 1 ORDER BY 1""", [])

    table(bq, "Pages: current vs previous window", win + f"""
      , agg AS (
        SELECT {page} AS pg,
          SUM(IF(data_date >= cur_start, impressions, 0)) AS ci,
          SUM(IF(data_date >= cur_start, clicks, 0)) AS cc,
          SUM(IF(data_date >= cur_start, sum_position, 0)) AS cp,
          SUM(IF(data_date <= prev_end, impressions, 0)) AS pi,
          SUM(IF(data_date <= prev_end, clicks, 0)) AS pc,
          SUM(IF(data_date <= prev_end, sum_position, 0)) AS pp
        FROM {u}, w WHERE data_date BETWEEN prev_start AND cur_end
        GROUP BY 1)
      SELECT pg AS page, ci AS impr, cc AS clicks,
             ROUND(SAFE_DIVIDE(cp, ci) + 1, 1) AS pos,
             pi AS prev_impr, pc AS prev_clicks,
             ROUND(SAFE_DIVIDE(pp, pi) + 1, 1) AS prev_pos
      FROM agg WHERE ci > 0 ORDER BY ci DESC LIMIT 40""", p)

    table(bq, "Top queries (current window)", win + f"""
      SELECT query, SUM(impressions) impr, SUM(clicks) clicks,
             ROUND(SUM(sum_top_position) / SUM(impressions) + 1, 1) pos
      FROM {s}, w WHERE data_date >= cur_start AND query IS NOT NULL
      GROUP BY 1 ORDER BY impr DESC LIMIT 50""", p)

    table(bq, "Query → page (which page Google shows for each query)", win + f"""
      SELECT query, {page} page, SUM(impressions) impr, SUM(clicks) clicks,
             ROUND(SUM(sum_position) / SUM(impressions) + 1, 1) pos
      FROM {u}, w WHERE data_date >= cur_start AND query IS NOT NULL
      GROUP BY 1, 2 HAVING impr >= 10 ORDER BY impr DESC LIMIT 60""", p)

    table(bq, "Striking distance: pos 4–20, ≥20 impressions, CTR < 2%", win + f"""
      SELECT * FROM (
        SELECT {page} AS page, query, SUM(impressions) AS impr, SUM(clicks) AS clk,
               ROUND(SUM(sum_position) / SUM(impressions) + 1, 1) AS pos
        FROM {u}, w WHERE data_date >= cur_start AND query IS NOT NULL
        GROUP BY 1, 2)
      WHERE impr >= 20 AND pos BETWEEN 4 AND 20 AND SAFE_DIVIDE(clk, impr) < 0.02
      ORDER BY impr DESC LIMIT 30""", p)

    table(bq, "Non-canonical URLs getting impressions (http://, no trailing slash, etc.)", win + f"""
      SELECT url, SUM(impressions) impr, SUM(clicks) clicks
      FROM {u}, w WHERE data_date >= cur_start
        AND NOT STARTS_WITH(url, '{SITE}/')
         OR (STARTS_WITH(url, '{SITE}/') AND data_date >= cur_start
             AND NOT ENDS_WITH(url, '/') AND NOT REGEXP_CONTAINS(url, r'\\.[a-z]+$'))
      GROUP BY 1 ORDER BY impr DESC LIMIT 20""", p)


if __name__ == "__main__":
    main()
