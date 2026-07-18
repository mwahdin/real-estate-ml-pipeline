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
