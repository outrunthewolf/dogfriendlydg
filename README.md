# Dog Friendly DG

A Jekyll-powered directory of dog-friendly places across Dumfries and Galloway, Scotland.

## About

Dog Friendly DG is a community resource for dog owners visiting or living in Dumfries and Galloway. The site covers:

- **Walks** -- from short hill strolls to full-day forest routes
- **Beaches** -- with clear notes on seasonal dog restrictions
- **Pubs & Cafes** -- genuinely dog-welcoming, not just tolerating
- **Accommodation** -- dog-friendly lodges, hotels, and B&Bs
- **Vets & Groomers** -- local services for dogs across the region

## Tech Stack

- [Jekyll](https://jekyllrb.com/) static site generator
- GitHub Pages compatible
- No JavaScript dependencies
- Vanilla CSS with mobile-first responsive layout

## Project Structure

```
dogfriendlydg/
├── _config.yml            # Jekyll site configuration
├── Gemfile                # Ruby gem dependencies
├── index.html             # Homepage (uses home layout)
├── README.md              # This file
├── robots.txt             # Search engine crawl rules
│
├── _layouts/
│   ├── default.html       # Base layout with nav and footer
│   ├── home.html          # Homepage layout with category grid
│   ├── listing.html       # Individual listing page layout
│   └── post.html          # Blog post layout
│
├── _listings/             # Jekyll collection: individual place listings
│   ├── glen-trool-walk.md
│   ├── murrays-monument-walk.md
│   ├── cardoness-castle-walk.md
│   ├── the-masonic-arms-gatehouse.md
│   ├── the-murray-arms-gatehouse.md
│   ├── sandgreen-beach.md
│   ├── mersehead-beach.md
│   ├── cream-o-galloway.md
│   ├── galloway-sailing-centre-accommodation.md
│   └── newton-stewart-dog-groomers.md
│
├── _posts/                # Blog posts (standard Jekyll)
│   ├── 2026-03-01-best-dog-walks-galloway-forest-park.md
│   ├── 2026-03-05-dog-friendly-beaches-solway-coast.md
│   ├── 2026-03-08-dog-friendly-pubs-gatehouse-fleet.md
│   ├── 2026-03-10-dog-friendly-day-out-castle-douglas-loch-ken.md
│   └── 2026-03-12-tips-for-visiting-dumfries-galloway-with-dogs.md
│
├── walks/
│   └── index.html         # Walks category listing page
├── beaches/
│   └── index.html         # Beaches category listing page
├── pubs-cafes/
│   └── index.html         # Pubs & cafes category listing page
├── accommodation/
│   └── index.html         # Accommodation category listing page
├── vets-groomers/
│   └── index.html         # Vets & groomers category listing page
└── events/
    └── index.html         # Events category listing page
```

## Listing Front Matter

Each listing in `_listings/` uses this front matter schema:

```yaml
---
layout: listing
title: "Place Name -- Location"
name: "Business/Place Name"
category: walk | beach | pub-cafe | accommodation | vet-groomer | event
address: "Street address"
town: "Town"
region: "Dumfries and Galloway"
postcode: "Postcode"
website: "https://..." or ""
phone: "Phone number" or ""
facilities: [facility one, facility two, facility three]
dogs_notes: "Specific dog-friendliness notes"
lat: 55.0000
lng: -4.0000
excerpt: "One sentence SEO excerpt for listing cards and meta description."
---
```

Followed by 200-300 words of useful, SEO-optimised body content.

## Running Locally

```bash
# Install dependencies
bundle install

# Serve locally with live reload
bundle exec jekyll serve --livereload

# Build for production
bundle exec jekyll build
```

The site will be available at `http://localhost:4000`.

## Adding New Listings

1. Create a new `.md` file in `_listings/`
2. Use the front matter schema above
3. Write 200-300 words of genuine, helpful body content
4. Add latitude/longitude coordinates (use Google Maps or OS grid converter)
5. Commit and push -- Jekyll rebuilds automatically on GitHub Pages

## Deployment

The site is designed for GitHub Pages deployment. Push to the `main` branch of a GitHub repository with Pages enabled, pointing to the root directory. No build configuration required beyond the `_config.yml`.

## Contributing

Suggestions for new listings are welcome. Please include full front matter details and accurate coordinates. All listings are manually reviewed before publication.

## Licence

Content copyright Dog Friendly DG. Jekyll theme and layout code available under MIT licence.
