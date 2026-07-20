import pandas as pd

df = pd.read_csv("data/data_numeric.csv")

print("=" * 50)
print("Shape")
print(df.shape)

print("=" * 50)
print("Missing Values")
print(df.isna().sum().sort_values(ascending=False).head(20))

print("=" * 50)
print("Dtypes")
print(df.dtypes)

print("=" * 50)
print("Duplicate Rows")
print(df.duplicated().sum())
import pandas as pd

df = pd.read_csv("data/data_numeric.csv")

for c in df.columns:
    if "بالکن" in c:
        print(c)