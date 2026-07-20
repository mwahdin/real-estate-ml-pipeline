import json
import pandas as pd

with open("data/raw/divar.json", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)

print(df.info())

print("\n========== Missing Values ==========\n")
print(df.isna().sum())

print("\n========== Columns ==========\n")
print(df.columns.tolist())

print("\n========== Shape ==========")
print(df.shape)

print("\n========== Duplicated Token ==========")
print(df["token"].duplicated().sum())

print("\n========== Duplicated URL ==========")
print(df["url"].duplicated().sum())

print("\n========== Business Types ==========")
print(df["business_type"].value_counts())

print("\n========== District Count ==========")
print(df["district"].nunique())

print("\n========== Top 20 Districts ==========")
print(df["district"].value_counts().head(20))

feature_keys = set()

for f in df["features"]:
    feature_keys.update(f.keys())

print("\n========== Feature Keys ==========")
print(sorted(feature_keys))


detail_keys = set()

for d in df["details"]:
    detail_keys.update(d.keys())

print("\n========== Detail Keys ==========")
print(sorted(detail_keys))