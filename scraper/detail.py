import json
from client import DivarClient

client = DivarClient()

token = "gaUVJ1NN"   # یا هر توکنی که از search گرفتی

detail = client.get_post_detail(token)

with open("detail.json", "w", encoding="utf-8") as f:
    json.dump(detail, f, ensure_ascii=False, indent=2)

print("saved detail.json")
