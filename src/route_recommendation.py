
import pandas as pd

# Step 1: Load scored dataset
df = pd.read_csv("data/scored_routes.csv")

print("SCORED DATASET LOADED SUCCESSFULLY")


# Step 2: Sort routes by shipment and weighted score
df = df.sort_values(
    by=["shipment_id", "weighted_score"],
    ascending=[True, True]
)


# Step 3: Select the best route for every shipment
best_routes = (
    df.groupby("shipment_id")
    .first()
    .reset_index()
)


# Step 4: Select top 3 routes for every shipment
top_three_routes = (
    df.groupby("shipment_id")
    .head(3)
    .copy()
)


# Step 5: Generate recommendation explanation
def generate_explanation(row):

    return (
        f"Route {row['route_id']} is recommended because "
        f"it has the lowest weighted score of "
        f"{row['weighted_score']:.4f} among the available "
        f"routes for shipment {row['shipment_id']}. "
        f"It provides the best overall balance according "
        f"to the selected cost, time and risk weights."
    )


best_routes["recommendation_reason"] = (
    best_routes.apply(generate_explanation, axis=1)
)


# Step 6: Display recommended routes
print("\nBEST ROUTE RECOMMENDATIONS:")

print(
    best_routes[[
        "shipment_id",
        "route_id",
        "cost",
        "transit_days",
        "weighted_score"
    ]].to_string(index=False)
)


# Step 7: Display top 3 alternatives for first 5 shipments
print("\nTOP 3 ROUTES FOR FIRST 5 SHIPMENTS:")

print(
    top_three_routes[[
        "shipment_id",
        "route_id",
        "cost",
        "transit_days",
        "risk_score",
        "weighted_score",
        "route_rank"
    ]].head(15).to_string(index=False)
)


# Step 8: Save recommendation results
best_routes.to_csv(
    "data/recommended_routes.csv",
    index=False
)

top_three_routes.to_csv(
    "data/top3_routes.csv",
    index=False
)


print("\nROUTE RECOMMENDATION COMPLETED SUCCESSFULLY!")

print("\nTotal shipments recommended:",
      len(best_routes))

print("\nFiles created:")
print("data/recommended_routes.csv")
print("data/top3_routes.csv")
