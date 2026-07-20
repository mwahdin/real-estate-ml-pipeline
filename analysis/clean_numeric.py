import pandas as pd
from scraper.utils import persian_to_number
from scraper.utils import parse_floor

df = pd.read_csv("data/data_clean.csv")
print(sorted(df["year"].unique()))
print(df.shape)

numeric_columns = [
    "area",
    "year",
    "rooms",
    "price_per_meter",
]

# تبدیل مقادیر
for col in numeric_columns:
    df[col] = df[col].apply(persian_to_number)

print(df[numeric_columns].dtypes)

print("\n========== Converted Values ==========\n")
print(df[numeric_columns].head(10))

print(df["floor"].value_counts().head(30))

df[["current_floor", "total_floors"]] = (
    df["floor"]
    .apply(parse_floor)
    .apply(pd.Series)
)

df.drop(columns=["floor"], inplace=True)

print(
    df[
        [
            "current_floor",
            "total_floors",
        ]
    ].head(20)
)
print(df.shape)

print(df.dtypes)

df.to_csv(
    "data/data_numeric.csv",
    index=False,
)

df.to_csv(
    "data/data_numeric.csv",
    index=False,
)

print("Saved -> data/data_numeric.csv")