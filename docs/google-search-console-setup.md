# Google Search Console Setup --- dogfriendlydg.co.uk

We need Chris to complete these steps to verify dogfriendlydg.co.uk in Google Search Console and activate SEO tracking.

Google Search Console (GSC) cannot be set up programmatically --- it requires you to log in with your Google account and complete a verification step. This document walks you through the exact steps.

---

## Step 1 --- Add the Property

1. Go to **https://search.google.com/search-console**
2. Sign in with the Google account you want to use for this site
3. Click **"Add property"** (top-left dropdown)
4. Choose **"Domain"** property type (NOT "URL prefix")
   - Domain type covers `http://`, `https://`, `www.` and non-`www.` all in one property
   - Enter: `dogfriendlydg.co.uk`
5. Click **Continue**

---

## Step 2 --- Verify Ownership

Google will offer several verification methods. For a GitHub Pages site, you have two good options:

### Option A --- DNS Verification (Recommended)

This is the cleanest method for GitHub Pages --- no files to upload.

1. Google will give you a TXT record to add to your DNS, e.g.:
   ```
   google-site-verification=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
   ```
2. Log in to your **domain registrar** (wherever you registered dogfriendlydg.co.uk)
3. Go to **DNS settings** and add a new **TXT record**:
   - **Type:** TXT
   - **Host / Name:** `@` (root domain)
   - **Value:** the verification string Google gives you
   - **TTL:** 3600 (or default)
4. Save and return to GSC
5. Click **Verify** --- DNS can take up to 24 hours to propagate but usually verifies within minutes

### Option B --- HTML File Upload

If you prefer not to touch DNS:

1. Google will give you a unique HTML filename, e.g.:
   ```
   googleXXXXXXXXXXXXXXXX.html
   ```
2. The file content is just a single line:
   ```
   google-site-verification: googleXXXXXXXXXXXXXXXX
   ```
3. This file needs to be in the **root of the GitHub repo** (`outrunthewolf/dogfriendlydg`)
4. Once you have your unique filename from GSC, let the site agent know and it will commit the file for you
5. Return to GSC and click **Verify**

---

## Step 3 --- Submit Your Sitemap

Once verified:

1. In the GSC left sidebar, go to **Sitemaps**
2. Enter the sitemap URL:
   ```
   sitemap.xml
   ```
   (Full URL: `https://dogfriendlydg.co.uk/sitemap.xml`)
3. Click **Submit**

The sitemap is generated automatically by the `jekyll-sitemap` plugin --- it will include all posts and listings.

---

## Step 4 --- What to Expect

| Timeframe | What GSC Will Show |
|-----------|---------------------|
| Day 1-3 | Property verified, sitemap submitted, pages queued for crawl |
| Week 1-2 | First impressions and clicks appear in Performance report |
| Week 3-4 | Coverage report shows indexed vs non-indexed pages |
| Month 1+ | Keyword data builds up --- use to guide future blog posts |

---

## Key GSC Reports to Check Weekly

- **Performance** --- which queries are bringing traffic, which pages rank
- **Coverage** --- confirms all posts and listings are indexed (no 404s or crawl errors)
- **Sitemaps** --- confirms sitemap is being processed
- **Core Web Vitals** --- page speed signals (GitHub Pages scores well here)

---

## Action Required from Chris

- [ ] Log in to https://search.google.com/search-console
- [ ] Add Domain property: `dogfriendlydg.co.uk`
- [ ] Choose DNS or HTML file verification method
- [ ] If HTML file: share the filename and the agent will commit it to the repo
- [ ] If DNS: add TXT record to your domain registrar
- [ ] Submit sitemap: `sitemap.xml`

---

*Created: 2026-03-17 | Site: dogfriendlydg.co.uk | Repo: outrunthewolf/dogfriendlydg*