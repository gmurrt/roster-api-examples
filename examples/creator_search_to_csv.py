import csv
import os
import time
import requests

api_key = os.environ.get("ROSTER_API_KEY", "").strip()
if not api_key or api_key == "YOUR_ROSTER_DATA_KEY":
    raise SystemExit("Set a real ROSTER_API_KEY in your local environment before running.")
headers = {"Authorization": f"Bearer {api_key}"}
params = {"niche": "fitness", "country": "US", "has_email": "true",
          "sort": "followers", "limit": 100}
fields = ["pk", "username", "follower_count", "extracted_email", "country"]
seen = set()

def spreadsheet_safe(value):
    text = str(value) if value is not None else ""
    if text.lstrip().startswith(("=", "+", "-", "@", "\t", "\r", "\n")):
        return "'" + text
    return text

with open("creators.csv", "w", newline="", encoding="utf-8") as output:
    writer = csv.DictWriter(output, fieldnames=fields)
    writer.writeheader()
    for page in range(1, 6):  # At most 5 requests / 50 search credits.
        response = requests.get(
            "https://api.ugcroster.com/v1/creators/search",
            headers=headers, params={**params, "page": page}, timeout=30)
        response.raise_for_status()  # Stop; do not retry indefinitely.
        payload = response.json()
        rows = payload["data"]
        for row in rows:
            if row["pk"] in seen:
                continue
            seen.add(row["pk"])
            writer.writerow({key: spreadsheet_safe(row.get(key)) for key in fields})
        if len(rows) < 100 or page * 100 >= payload["pagination"]["total"]:
            break
        time.sleep(1.1)  # Allow for other traffic sharing your key's limit.
