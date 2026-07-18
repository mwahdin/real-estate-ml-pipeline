import json
from parser import parse_post

with open("detail.json", encoding="utf-8") as f:
    detail = json.load(f)

data = parse_post(detail)

print(json.dumps(data, ensure_ascii=False, indent=2))