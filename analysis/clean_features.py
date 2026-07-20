import json
import pandas as pd

# -----------------------------
# Load dataset
# -----------------------------
df = pd.read_csv("data/data.csv")

# تبدیل رشته JSON به dict
df["features"] = df["features"].apply(json.loads)
df["details"] = df["details"].apply(json.loads)

# -----------------------------
# Flatten features/details
# -----------------------------
features_df = pd.json_normalize(df["features"])
details_df = pd.json_normalize(df["details"])

df = pd.concat(
    [
        df.drop(columns=["features", "details"]),
        features_df,
        details_df,
    ],
    axis=1,
)

print("Shape after flatten:", df.shape)

# -----------------------------
# Merge positive/negative columns
# -----------------------------
pairs = [
    ("آسانسور", "آسانسور ندارد"),
    ("پارکینگ", "پارکینگ ندارد"),
    ("انباری", "انباری ندارد"),
    ("بالکن", "بالکن ندارد"),
]

for positive, negative in pairs:

    if positive not in df.columns or negative not in df.columns:
        continue

    # NaN -> False
    pos = df[positive].fillna(False).astype(bool)

    # NaN -> False
    neg = df[negative].fillna(False).astype(bool)

    # اگر ستون مثبت True باشد همان True
    # اگر ستون منفی True باشد => False
    df[positive] = pos | (~neg)

    df.drop(columns=[negative], inplace=True)

# ------------------------
# Merge Balcony Columns
# ------------------------

if "بالکن دارد" in df.columns and "بالکن ندارد" in df.columns:

    df["بالکن"] = (
        df["بالکن دارد"]
        .fillna(False)
        .astype(bool)
    )

    df.drop(
        columns=["بالکن دارد", "بالکن ندارد"],
        inplace=True,
    )

print("Shape after cleaning:", df.shape)

# -----------------------------
# Save cleaned dataset
# -----------------------------
df.to_csv(
    "data/data_clean.csv",
    index=False,
    encoding="utf-8-sig"
)

print("Saved -> data/data_clean.csv")