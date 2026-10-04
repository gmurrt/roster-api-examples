# Find creator profiles by niche and country with the Roster API

## Who is this for?

Marketing operations teams and developers building creator shortlists in n8n. Start with a single manual request, inspect the response, then decide how to connect the results to your own workflow.

## What it does

This workflow searches Roster's stored creator directory for a niche and creator country. The example searches for US fitness creators and requests up to 20 results. It returns the API's JSON response so you can inspect profile fields before adding a spreadsheet, CRM or other destination.

The workflow has a manual trigger, a setup note and one HTTP Request node. It does not send messages, fetch additional profiles or paginate automatically.

## Set up

1. Import the attached `creator-search.json` workflow into n8n.
2. Get a Roster data key from https://api.ugcroster.com/keys. Check current access requirements and prices at https://api.ugcroster.com/pricing.
3. Open **Search creators — 10 credits** and create or select a **Header Auth** credential. Set its name to `Authorization` and its value to `Bearer YOUR_ROSTER_DATA_KEY`, replacing the placeholder inside n8n's credential store.
4. Review `q=fitness`, `country=US`, `page=1` and `limit=20` in the request's query parameters.
5. Run manually and inspect the returned JSON.

## Cost and customization

Prepaid access starts at $25 for 5,000 credits, without a monthly subscription, at 60 requests/minute. Credit purchases are manual; there is no automatic recharge. Existing subscribers retain their current terms.

Each manual execution makes one search request and uses 10 Roster credits. It returns up to 20 matching records; fewer, including zero, may match. Automatic retries and pagination are disabled. Changing the result limit does not introduce additional pages. If you later add a schedule or pagination, set a recurring request budget first.

No API key, pinned creator data or saved credentials are included. The workflow imports inactive. The HTTP Request node uses type version 4.2.

Creator country describes creator location, not audience geography. Profiles are stored directory records, not a new live scrape. A published email does not establish deliverability or permission to contact someone.

API reference: https://api.ugcroster.com/docs
Integration guide: https://api.ugcroster.com/integrations/http
Source: https://github.com/gmurrt/roster-api-examples/blob/main/n8n/creator-search.json
