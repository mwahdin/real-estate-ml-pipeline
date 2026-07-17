import requests
import csv


def persian_to_number(text):
    if not text:
        return None

    # تبدیل اعداد فارسی به انگلیسی
    persian_digits = "۰۱۲۳۴۵۶۷۸۹"
    english_digits = "0123456789"

    for p, e in zip(persian_digits, english_digits):
        text = text.replace(p, e)

    text = text.replace("٫", ".").replace(",", "")

    # تبدیل میلیارد و میلیون
    if "میلیارد" in text:
        return float(text.replace("میلیارد", "").strip()) * 1_000_000_000
    elif "میلیون" in text:
        return float(text.replace("میلیون", "").strip()) * 1_000_000

    return float(text)


def extract_number(text):
    if not text:
        return None

    persian_digits = "۰۱۲۳۴۵۶۷۸۹"
    english_digits = "0123456789"

    for p, e in zip(persian_digits, english_digits):
        text = text.replace(p, e)

    digits = "".join(filter(str.isdigit, text))

    return int(digits) if digits else None


class DivarClient:
    BASE_URL = "https://api.divar.ir"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/138.0.0.0 Safari/537.36"
                ),
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

    def viewport(self, payload: dict):
        url = f"{self.BASE_URL}/v8/mapview/viewport"
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    def get_post_detail(self, token: str):
        url = f"{self.BASE_URL}/v8/posts/{token}"
        response = self.session.get(url)
        print(response.status_code)
        print(response.text)
        response.raise_for_status()
        return response.json()

    def search(self, payload: dict):
        url = f"{self.BASE_URL}/v8/postlist/w/search"
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()


# 👇 این تابع باید بیرون کلاس باشه
def parse_post(detail):
    data = {}

    data["title"] = detail.get("data", {}).get("title")

    sections = detail.get("data", {}).get("sections", [])

    for section in sections:
        for widget in section.get("widgets", []):
            if widget.get("widget_type") == "LIST_DATA":
                for item in widget.get("data", {}).get("items", []):
                    title = item.get("title")
                    value = item.get("value")

                    if title == "قیمت کل":
                        data["price"] = value
                    elif title == "متراژ":
                        data["area"] = value
                    elif title == "تعداد اتاق":
                        data["rooms"] = value

    return data


client = DivarClient()
payload = {
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

seen_tokens = set()
all_rows = []
last_post_date = None


page = 1

while True:

    data = client.search(payload)
    print(data["pagination"])
    widgets = data.get("list_widgets", [])

    print(f"PAGE {page}")

    for widget in widgets:

        if widget.get("widget_type") != "POST_ROW":
            continue

        d = widget["data"]

        token = (
            d.get("action", {})
             .get("payload", {})
             .get("token")
        )

        if token in seen_tokens:
            continue

        seen_tokens.add(token)

        row = {
            "token": token,
            "title": d.get("title"),
            "price": d.get("middle_description_text"),
            "agency": d.get("bottom_description_text"),
            "image": d.get("image_url"),
        }

        all_rows.append(row)
        print(row["title"])

    print("TOTAL:", len(all_rows))

    with open("data.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=all_rows[0].keys())
        writer.writeheader()
        writer.writerows(all_rows)

    print("saved.")

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

    page += 1
print("TOTAL ROWS:", len(all_rows))
print("UNIQUE TOKENS:", len(set(r["token"] for r in all_rows)))