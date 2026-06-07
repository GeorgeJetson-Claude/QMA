# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

QuoteMyAnything (QMA) is a **static marketing/lead-generation website** plus a set
of **Python "organic lead" agents**. The product is a "get 3 free local quotes"
funnel for home services (roofing, HVAC, plumbing, solar, etc.), starting in
Austin TX and expanding city-by-city. The business strategy, revenue model, and
roadmap are the real source of truth and live in `PLAN.md` — read it before making
product/content decisions. Brand rules are in `BRAND_GUIDELINES.md` and are
binding for any visible copy, color, or asset change.

There is **no build step, no package manager, no test suite, no framework**. Pages
are hand-written HTML using the Tailwind CDN. Deployment is git-push → Vercel.

## Repository layout

- **`/*.html`** (repo root) — the live site. Two page types:
  - **Service landing pages** (`roofing.html`, `hvac.html`, `plumbing.html`,
    `solar.html`, `lawn-care.html`, `painting.html`, `electrical.html`,
    `pest-control.html`, `tree-service.html`, `moving.html`,
    `house-cleaning.html`, `business-insurance.html`) — each has a Formspree lead
    form and shares the same header/footer/consent/chat structure as `index.html`.
  - **Calculators / lead-magnet tools** (`roof-calculator.html`,
    `hvac-calculator.html`, `solar-calculator.html`, `painting-calculator.html`,
    `moving-estimator.html`, `electrical-estimator.html`, `car-ai-guide.html`) —
    interactive client-side estimators with no signup.
  - `index.html` is the homepage; `for-pros.html` is the contractor-facing
    console/pricing page; `dashboard.html` is an internal `noindex` page.
  - Legal pages: `privacy.html`, `terms.html`, `disclaimer.html`.
  - `*.bak` files are stale backups — ignore them.
- **`assets/`** — `logos/`, `gemini/` (brand video, the primary brand asset),
  `ads/`, `jingles/`, `js/qma-chat.js` (the chat widget), and business-plan docx
  files.
- **`quotemyanything-social/agents/`** — Python lead-finding/routing agents (see
  below).
- **`projects/quotemyanything/`** — older/duplicate copies of some pages plus
  business notes (`QMA_PROJECT_NOTES.md`, `IP_PROTECTION_BUSINESS_REGISTRATION.md`).
  Not deployed; the deployed site is the repo root. Don't edit these expecting
  them to go live.
- **Markdown playbooks** at root — `PLAN.md` (master plan), `OPERATIONS.md`,
  `LEAD_SYSTEM.md`, `BRAND_GUIDELINES.md`, `LAUNCH_CHECKLIST.md`, `SITE_REVIEW.md`,
  `ZAPIER_SETUP.md`, `FUNDING_AND_EIN_CHECKLIST.md`. These are operational docs,
  not code.

## Deploy / run

- **Deploy:** push to `main` → GitHub Action `.github/workflows/deploy.yml` runs
  `vercel pull` then `vercel deploy --prod` to the QMA Vercel project (org/project
  IDs are in the workflow; token is the `VERCEL_TOKEN` repo secret). There is no
  other build. Production domain: `quotemyanything.com`.
- **Preview locally:** it's plain static HTML — open a file in a browser, or serve
  the repo root with any static server, e.g. `python3 -m http.server 8000`.
- **Run the lead agents** (from `quotemyanything-social/agents/`, stdlib-only,
  no deps, no API keys):
  - `python3 daily_workflow.py --service roofing` — fetch organic leads → route →
    draft replies → log to `leads_log.jsonl`.
  - `python3 storm_roof_agent.py [service]` — full daily run (Reddit scan + social
    copy + checklist).
  - `python3 zap_sim_organic.py` — Reddit buying-intent finder → `leads_log.txt`.
  - `python3 lead_router.py --input leads.csv --output routed_leads.json` — route
    a CSV of leads to contractors.

## How the lead system fits together

1. **Capture:** every public page posts to **Formspree** (free tier). Form IDs:
   `xpwzgqkd` (service requests) and `xdajvlvr` (main form). These IDs are wired
   into the HTML `<form action>` attributes — keep them consistent if you add a
   page.
2. **Route:** `lead_router.py` maps free-text service + ZIP → a contractor in the
   hard-coded `CONTRACTOR_DB` (currently placeholder Austin `.local` emails).
   `SERVICE_MAP` translates keywords ("hail", "shingle" → roofing, etc.) — this
   same keyword→service mapping is duplicated in `zap_sim_organic.py` and
   `assets/js/qma-chat.js`; keep them in sync when adding a service.
3. **Find (organic):** the agents scan Reddit `/new.json` across home-service
   subreddits (`channels.json`) for buying-intent posts and **draft** replies.
   **Human-in-the-loop is intentional and non-negotiable** — agents never
   auto-post (it gets accounts banned and burns the brand). They surface
   opportunities; a human posts by hand.
4. **Forward:** routing to contractors / Google Sheets is currently manual or via
   Zapier (Formspree → Sheets/email). See `LEAD_SYSTEM.md` / `OPERATIONS.md`.

## Site conventions (match these when editing or adding pages)

- **Dark theme is the brand.** Body is `bg-zinc-950 text-zinc-100`; palette and
  exact hexes are locked in `BRAND_GUIDELINES.md` (emerald `#10b981` = trust/free
  CTAs; amber `#f59e0b` = service-page submit buttons). Don't introduce new colors.
- **Tailwind via CDN** (`<script src="https://cdn.tailwindcss.com">`) — no build,
  no config file. Use utility classes inline.
- **SEO is load-bearing.** Pages carry hand-written `<title>`/`description`/
  `keywords`, a `<link rel="canonical">`, and JSON-LD schema (`Organization`,
  `Service`, `FAQPage`). When adding/duplicating a page, update the canonical URL,
  schema, and `sitemap.xml`. `robots.txt` and `sitemap.xml` are maintained by hand.
- **City expansion:** to launch a new city, duplicate pages and swap only the city
  name in titles/H1/schema and the local subreddits/GBP — keep everything else
  identical (one brand, many cities). See `BRAND_GUIDELINES.md` §9.
- **Chat widget:** `assets/js/qma-chat.js` is a self-contained, rule-based,
  backend-less assistant added before `</body>`. It routes visitors to the right
  service page. Upgrade path (Grok/Claude API) is documented in the file header —
  don't add a paid backend without revenue justification.
- **Internal dashboard:** `dashboard.html` is `noindex,nofollow` and reached only
  via a covert 3-click sequence on the homepage copyright text
  (`handleSecretClick` in `index.html`). There is intentionally no public link.
- **Privacy/compliance is part of the brand promise:** TCPA consent line on every
  lead form, "Reply STOP to unsubscribe," and Privacy/Terms/Disclaimer linked in
  every footer. Analytics are privacy-first via `localStorage` only — no
  third-party trackers. Never publish an unverified phone number or a home address
  (use a virtual address). These rules are enforced in `PLAN.md` and
  `BRAND_GUIDELINES.md`.
