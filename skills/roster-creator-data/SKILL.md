---
name: roster-creator-data
description: Search the Roster creator directory or retrieve stored creator profiles when a user requests creator discovery or directory enrichment. Requires a configured Roster data key and an authorized credit budget.
---

# Roster creator data

Use only for relevant creator discovery and directory profile lookup tasks.
Do not call this service for unrelated research, automatically on startup, or simply because it is installed.
Do not substitute it for audience demographics, live scraping, email validation, or creator outreach.

## Connection

Remote MCP: https://api.ugcroster.com/v1/mcp (Streamable HTTP).
REST base: https://api.ugcroster.com/v1.
Authentication: Authorization: Bearer <data key>. Read secrets from the configured credential store; never print or commit them.
Docs: https://api.ugcroster.com/docs.
Current capabilities/pricing: https://api.ugcroster.com/capabilities.json.
Use search_creators, get_creator and get_usage only. Other tools require a separate brand key.

## Before spending

Respect any existing user authorization and budget. If the task does not authorize paid data access, explain the proposed request and obtain authorization before a metered call.
Read the current manifest for credit costs. Currently one search page costs 10 credits and one profile read costs 1 credit. get_usage costs zero credits.
Compute the maximum job cost: pages * search_page_credits + profile_reads * profile_read_credits, counting every attempted retry conservatively.
An active paid API subscription is required; credits are not a per-call cash price. Never buy credits or change plans from this skill.
Use get_usage to check the available balance before an authorized batch. Do not poll repeatedly.

## Execution

Default proposed job: one search page, limit 20, zero profile reads, zero retries. Request more only when required by the task and inside the authorized budget.
Apply the user's niche, follower and creator-location filters. Do not invent audience filters or IDs. Consult the reference for supported parameters.
Deduplicate by pk and reuse fields already returned by search.
Read an individual profile only when needed, using its pk from search results.
Stop on the budget limit, adequate results, an empty page, authentication error, exhausted credits or rate-limit response. Do not silently broaden the search or continue pagination.
On a timeout, report uncertain consumption; do not automatically retry a potentially billed request.
For unattended jobs, implement a maximum request counter in application code. This skill itself does not enforce a server-side budget.

## Output

Return the relevant available fields, the number of calls attempted and the estimated credits consumed. Use the usage endpoint once after the job if exact account usage reconciliation is needed; concurrent jobs can affect the delta.
State missing information. Stored records are not guaranteed fresh. Creator location is not audience location; an email on file is not verified deliverability.
Never send messages, hire creators, create campaigns, or initiate payouts as part of a directory task.
