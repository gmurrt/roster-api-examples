# Roster Creator API Examples

Bounded examples for searching creator records and retrieving stored profiles through the [Roster Creator Data API](https://api.ugcroster.com). Use them to build shortlists, CSV exports and creator-data integrations.

## Start without an API key

- [Request builder](https://api.ugcroster.com/tools/request-builder): generate cURL or Python and preview the maximum credit cost. Does not execute requests.
- [Data quality sample inspector](https://api.ugcroster.com/tools/data-quality): inspect your JSON locally for duplicate IDs and missing fields. Does not upload records.
- [Usage calculator](https://api.ugcroster.com/pricing#calculator): compare monthly plans and prepaid top-ups.
- [Workflow recipes](https://api.ugcroster.com/use-cases) and [API reference](https://api.ugcroster.com/docs).

## What the API provides

`GET https://api.ugcroster.com/v1/creators/search` searches stored creator records. Supported filters include niche, creator country, follower bounds and the presence of a contact email. Search results include profile fields, so there is often no need for a second read.

`GET https://api.ugcroster.com/v1/creators/{pk}` retrieves one stored creator profile. Use a numeric `pk` returned by search; a username is not a primary key.

Creator location is not audience geography. A published email does not establish deliverability, permission to contact, availability or commercial fit. Reading a profile does not initiate a live social-platform scrape. Matching results may be fewer than requested, including zero. These examples do not contact creators.

## Authentication and current pricing

Create a data key in the [API console](https://api.ugcroster.com/keys). Requests use `Authorization: Bearer <data key>`. An active paid API subscription is required. Do not commit or paste real keys into shared examples.

Public pricing checked October 4, 2026:

| Plan | Monthly subscription (USD) | Monthly credits | Requests / minute |
| --- | ---: | ---: | ---: |
| Starter | $98 | 25,000 | 60 |
| Growth | $398 | 150,000 | 120 |
| Scale | $998 | 500,000 | 300 |

One search page costs **10 credits**, with up to 100 results per page. One profile read costs **1 credit**, including an unknown ID. Top-ups start at **$25 for 5,000 credits**, alongside an active subscription. These are credit allocations, not per-call cash checkout prices. Check [current pricing](https://api.ugcroster.com/pricing) and the [machine-readable capability manifest](https://api.ugcroster.com/capabilities.json) before running production jobs.

## Python: search to CSV

Requirements: Python 3.9+ and `requests`. From this repository directory:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

Edit the ignored `.env` file locally and replace the placeholder. It must contain only your trusted local assignment. Then load it and run:

```sh
set -a
. ./.env
set +a
python examples/creator_search_to_csv.py
```

The script searches for US fitness creators with contact emails and writes `creators.csv` locally. Edit the `params` dictionary to change the filters before running.

- Maximum **5 search requests / 50 credits per run**.
- Up to **500 rows before deduplication**; fewer may match.
- Stops early on an empty/short page or when the reported total is reached.
- Deduplicates by `pk`; escapes spreadsheet formula prefixes in CSV fields.
- Stops on HTTP errors; no automatic retries or profile reads.
- Uses a 30-second request timeout and pauses between pages. Other traffic sharing your key still counts toward your rate limit.

Every rerun starts a new budget and overwrites `creators.csv`. A timeout can leave consumption uncertain; check account usage before retrying. The directory can change between pages, so pagination is not a snapshot and can skip records even with deduplication.

To validate syntax without making any API request:

```sh
python3 -m py_compile examples/creator_search_to_csv.py
```

## n8n: one manual creator search

Import `n8n/creator-search.json` into n8n. In the HTTP Request node, choose or create a **Header Auth** credential:

- Name: `Authorization`
- Value: `Bearer YOUR_ROSTER_DATA_KEY` (replace locally in n8n's credential store)

Review `q=fitness`, `country=US`, `page=1` and `limit=20` before running manually. The workflow is inactive on import and has no saved credentials or example customer records.

Each manual execution makes **one search request / 10 credits**, returning up to 20 results. Automatic retries and pagination are disabled. The exported workflow uses HTTP Request node type version 4.2; inspect the imported node before execution if your n8n version differs. Do not add a schedule until you have set an appropriate recurring budget.

Validate the file locally:

```sh
python3 -m json.tool n8n/creator-search.json > /dev/null
```

## Optional agent skill

`skills/roster-creator-data/SKILL.md` describes narrowly scoped creator discovery and profile lookup. Install it using your agent's documented local-skill mechanism. Installing the text does not connect an account or grant a spending budget.

The skill requires relevant user intent, a configured data key and authorization for paid access. It proposes one search page by default, checks usage once and avoids automatic retries. A skill is guidance, not a server-enforced spending cap; enforce request limits in application code for unattended jobs.

Remote MCP endpoint: `https://api.ugcroster.com/v1/mcp` (Streamable HTTP). The data-key tools are `search_creators`, `get_creator` and `get_usage`; other campaign tools require a separate brand key. [Connection instructions](https://api.ugcroster.com/integrations).

## License

MIT. The software license does not grant rights to API data or replace the service terms. No real creator records, credentials or customer data are included in this repository.
