import json
import pandas as pd

with open("data/raw/divar.json", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)

print(df.shape)

features_df = pd.json_normalize(df["features"])

print(features_df.head())

details_df = pd.json_normalize(df["details"])

print(details_df.head())

# حذف ستون‌های دیکشنری
df = df.drop(columns=["features", "details"])

# اضافه کردن ستون‌های باز شده
df = pd.concat(
    [
        df,
        features_df,
        details_df
    ],
    axis=1
)

print(df.shape)
print(df.columns.tolist())
print(df[["آسانسور", "آسانسور ندارد"]].head(20))
print("\nآسانسور")
print(df["آسانسور"].value_counts(dropna=False))

print("\nآسانسور ندارد")
print(df["آسانسور ندارد"].value_counts(dropna=False))