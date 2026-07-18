import csv
import json
import os
import copy
import time
import random

from scraper.client import DivarClient
from scraper.parser import parse_post

AUTOSAVE_EVERY = 100

PAYLOAD = {
    "city_ids": ["904"],
    "source_view": "MAP_DISCOVERY_MAP",
    "pagination_data": {
        "@type": "type.googleapis.com/post_list.PaginationData",
        "last_post_date": "2026-07-17T17:10:19.629545Z",
        "page": 1,
        "layer_page": 1,
        "search_uid": "1d777b74-8919-46da-aafb-1df404fd15a2",
        "cumulative_widgets_count": 26,
        "viewed_tokens": "H4sIAAAAAAAE/xzOTU+DQBDG8S80B5W2LkdX26XErgXZN28jmMHISwSULJ/ejLdf/s9hhjA0GR3egRDTcCMrht2Ljx0Qvsj7wzVy6cZWDUBol4cqlFz0eUtmhh03oxhp8qw0EFZ6lpdHIIyrv8Sap84PQjCsb/IvRumXNGfkflfzLZT+iBOX217FVyD8OWbJ9ZtL6+bfFQjrwjztP4HQnAvnWp7elMj+n9d3p8kAIZ5U78JfAAAA///wGX8R1wAAAA==",
        "search_bookmark_info": {
            "search_hash": "bb90ad2a732e139a8875f13087c322e9",
            "bookmark_state": {},
            "alert_state": {},
        },
        "first_page_viewed_at": "2026-07-17T21:49:05.905910932Z",
    },
    "disable_recommendation": False,
    "map_state": {"camera_info": {"bbox": {}}},
    "search_data": {
        "form_data": {
            "data": {
                "sort": {"str": {"value": "sort_date"}},
                "category": {"str": {"value": "apartment-sell"}},
                "bbox": {
                    "repeated_float": {
                        "value": [
                            {"value": 51.37463},
                            {"value": 35.6656647},
                            {"value": 51.4176064},
                            {"value": 35.7501259},
                        ]
                    }
                },
                "map_free_roaming": {"boolean": {"value": True}},
            }
        },
        "server_payload": {
            "@type": "type.googleapis.com/widgets.SearchData.ServerPayload",
            "additional_form_data": {},
        },
    },
}


def save_dataset(all_rows):
    csv_rows = []

    for row in all_rows:
        r = row.copy()

        r["features"] = json.dumps(r.get("features", {}), ensure_ascii=False)

        r["details"] = json.dumps(r.get("details", {}), ensure_ascii=False)

        csv_rows.append(r)

    if csv_rows:
        os.makedirs("data", exist_ok=True)
        with open("data/data.csv", "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=csv_rows[0].keys())
            writer.writeheader()
            writer.writerows(csv_rows)

    os.makedirs("data/raw", exist_ok=True)

    with open("data/raw/divar.json", "w", encoding="utf-8") as f:
        json.dump(all_rows, f, ensure_ascii=False, indent=2)


def save_pagination(pagination_data):
    os.makedirs("data", exist_ok=True)

    with open("data/pagination.json", "w", encoding="utf-8") as f:
        json.dump(
            pagination_data,
            f,
            ensure_ascii=False,
            indent=2
        )

def load_dataset():

    path = "data/raw/divar.json"

    if not os.path.exists(path):
        return []

    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print("Dataset is corrupted.")
            return []

def load_pagination():

    path = "data/pagination.json"

    if not os.path.exists(path):
        return None

    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print("Pagination file is corrupted.")
            return None



def main():
    start = time.time()
    client = DivarClient()
    payload = copy.deepcopy(PAYLOAD)

    all_rows = load_dataset()

    seen_tokens = {
        row["token"]
        for row in all_rows
    }

    pagination = load_pagination()

    if pagination:
        payload["pagination_data"] = pagination

    print(f"Loaded {len(seen_tokens)} tokens.")
    print(f"Loaded {len(all_rows)} rows.")

    page = payload["pagination_data"]["page"]

    while True:

        while True:
            try:
                data = client.search(payload)
                break
            except Exception as e:
                print(f"Search Error: {e}")
                print("Retrying in 30 sec...")
                time.sleep(30)

        widgets = data.get("list_widgets", [])

        print(f"PAGE {page}")

        for widget in widgets:

            if widget.get("widget_type") != "POST_ROW":
                continue

            token = (
                widget.get("data", {})
                .get("action", {})
                .get("payload", {})
                .get("token")
            )

            if token in seen_tokens:
                continue
            if token in seen_tokens:
                continue

            success = False

            for attempt in range(5):

                try:
                    time.sleep(random.uniform(1, 2))

                    detail = client.get_post_detail(token)

                    row = parse_post(detail)
                    row["token"] = token

                    all_rows.append(row)
                    seen_tokens.add(token)

                    print(
                        f"[{len(all_rows)}] {row['title']}"
                    )

                    if len(all_rows) % AUTOSAVE_EVERY == 0:
                        save_dataset(all_rows)
                        save_pagination(payload["pagination_data"])
                        print(f"Autosaved {len(all_rows)} posts.")

                    success = True
                    break

                except Exception as e:

                    if "429" in str(e):
                        wait = 2 ** attempt * 10
                        print(f"429 Rate Limit - waiting {wait} sec...")
                        time.sleep(wait)
                    else:
                        print(f"Error on {token}: {e}")
                        break

            if not success:
                continue

        pagination = data.get("pagination")

        if not pagination:
            break

        if not pagination.get("has_next_page"):
            break

        print(
            pagination["data"]["page"],
            pagination["data"]["last_post_date"]
        )

        payload["pagination_data"] = pagination["data"]

        save_dataset(all_rows)
        save_pagination(payload["pagination_data"])

        print("Sleeping before next page...")
        time.sleep(random.uniform(5, 10))

        page = payload["pagination_data"]["page"]

    elapsed = time.time() - start

    print(f"Collected: {len(all_rows)}")
    print(f"Time: {elapsed/60:.1f} minutes")
    save_dataset(all_rows)
    save_pagination(payload["pagination_data"])

    print("saved.")
    print("TOTAL ROWS:", len(all_rows))
    print(f"Collected: {len(all_rows)}")


if __name__ == "__main__":
    main()
