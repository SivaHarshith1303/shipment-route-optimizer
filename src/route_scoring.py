
import pandas as pd

# Step 1: Load normalized dataset
df = pd.read_csv("data/normalized_routes.csv")

print("NORMALIZED DATASET LOADED SUCCESSFULLY")


# Step 2: Assign weights
COST_WEIGHT = 0.40
TIME_WEIGHT = 0.30
RISK_WEIGHT = 0.30


# Step 3: Calculate weighted score
df["weighted_score"] = (

    COST_WEIGHT * df["cost_norm"] +

    TIME_WEIGHT * df["time_norm"] +

    RISK_WEIGHT * df["risk_norm"]

)


# Step 4: Rank routes for each shipment
df["route_rank"] = (

    df.groupby("shipment_id")["weighted_score"]

    .rank(method="min", ascending=True)

)


# Step 5: Sort routes by shipment and score
df = df.sort_values(
    by=["shipment_id", "weighted_score"]
)


# Step 6: Display route scores
print("\nWEIGHTED SCORING RESULTS:")

print(
    df[[
        "shipment_id",
        "route_id",
        "cost",
        "transit_days",
        "risk_score",
        "weighted_score",
        "route_rank"
    ]].head(15)
)


# Step 7: Save scored dataset
df.to_csv(
    "data/scored_routes.csv",
    index=False
)


print("\nWEIGHTED SCORING COMPLETED SUCCESSFULLY!")

print("\nWeights Used:")
print("Cost:", COST_WEIGHT)
print("Time:", TIME_WEIGHT)
print("Risk:", RISK_WEIGHT)

print("\nScored dataset saved as:")
print("data/scored_routes.csv")
