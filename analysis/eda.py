import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("data/data_numeric.csv")

print(df.shape)

numeric_cols = [
    "price_number",
    "price_per_meter",
    "area",
    "year",
    "rooms",
    "current_floor",
    "total_floors",
]

print(df[numeric_cols].describe())

df["price_number"].hist(bins=50)

plt.title("Price Distribution")
plt.xlabel("Price")
plt.ylabel("Count")

plt.show()


plt.figure(figsize=(8,5))
plt.hist(df["area"], bins=40)
plt.title("Area Distribution")
plt.xlabel("Area")
plt.show()


plt.figure(figsize=(8,5))
plt.hist(df["price_per_meter"], bins=50)
plt.title("Price per Meter")
plt.show()


df["rooms"].value_counts().sort_index().plot(kind="bar")
plt.title("Rooms")
plt.show()


df["current_floor"].value_counts().sort_index().plot(kind="bar")
plt.title("Current Floor")
plt.show()


plt.figure(figsize=(8,6))
plt.scatter(
    df["area"],
    df["price_number"],
    alpha=0.3
)

plt.xlabel("Area")
plt.ylabel("Price")
plt.title("Area vs Price")

plt.show()