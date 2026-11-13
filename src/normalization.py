
import pandas as pd

# Step 1: Load the original dataset
df = pd.read_csv("data/shipment_routes.csv")

print("ORIGINAL DATASET LOADED SUCCESSFULLY")


# Step 2: Calculate overall risk
df["risk_score"] = (
    0.5 * df["delay_probability"] +
    0.3 * df["congestion_risk"] +
    0.2 * df["geopolitical_risk"]
)


# Step 3: Define Min-Max normalization function
def normalize(column):

    min_value = column.min()
    max_value = column.max()

    if max_value == min_value:
        return pd.Series(0.0, index=column.index)

    return (column - min_value) / (max_value - min_value)


# Step 4: Normalize cost, time and risk
# Compare routes belonging to the same shipment

df["cost_norm"] = (
    df.groupby("shipment_id")["cost"]
    .transform(normalize)
)

df["time_norm"] = (
    df.groupby("shipment_id")["transit_days"]
    .transform(normalize)
)

df["risk_norm"] = (
    df.groupby("shipment_id")["risk_score"]
    .transform(normalize)
)


# Step 5: Display normalized values
print("\nNORMALIZED DATASET:")

print(
    df[[
        "shipment_id",
        "route_id",
        "cost",
        "transit_days",
        "risk_score",
        "cost_norm",
        "time_norm",
        "risk_norm"
    ]].head(10)
)


# Step 6: Save normalized dataset
df.to_csv(
    "data/normalized_routes.csv",
    index=False
)


print("\nNORMALIZATION COMPLETED SUCCESSFULLY!")

print("\nNormalized dataset saved as:")
print("data/normalized_routes.csv")
