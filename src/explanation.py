
import pandas as pd

# Step 1: Load scored dataset
df = pd.read_csv("data/scored_routes.csv")

print("SCORED DATASET LOADED SUCCESSFULLY")


# Step 2: Create a list to store explanations
results = []


# Step 3: Process each shipment separately
for shipment_id, group in df.groupby("shipment_id"):

    # Recommended route: minimum weighted score
    recommended = group.loc[group["weighted_score"].idxmin()]

    # Cheapest route
    cheapest = group.loc[group["cost"].idxmin()]

    # Fastest route
    fastest = group.loc[group["transit_days"].idxmin()]

    # Lowest overall risk route
    safest = group.loc[group["risk_score"].idxmin()]

    # Step 4: Generate explanation
    explanation = (
        f"Route {recommended['route_id']} is recommended "
        f"for shipment {shipment_id} because it has the "
        f"lowest weighted score of "
        f"{recommended['weighted_score']:.4f}. "
    )

    # Compare with cheapest route
    if recommended["route_id"] == cheapest["route_id"]:
        explanation += (
            f"It is also the cheapest option at "
            f"Rs. {recommended['cost']}. "
        )
    else:
        difference = (
            recommended["cost"] - cheapest["cost"]
        )

        explanation += (
            f"The cheapest option is Route "
            f"{cheapest['route_id']} at Rs. "
            f"{cheapest['cost']}. The recommended "
            f"route costs Rs. {difference:.0f} more. "
        )

    # Compare with fastest route
    if recommended["route_id"] == fastest["route_id"]:
        explanation += (
            f"It is also the fastest option, taking "
            f"{recommended['transit_days']} days. "
        )
    else:
        difference = (
            recommended["transit_days"] -
            fastest["transit_days"]
        )

        explanation += (
            f"The fastest option is Route "
            f"{fastest['route_id']} taking "
            f"{fastest['transit_days']} days. "
            f"The recommended route takes "
            f"{difference} more "
            f"{'day' if difference == 1 else 'days'}. "
        )

    # Compare with lowest-risk route
    if recommended["route_id"] == safest["route_id"]:
        explanation += (
            "It also has the lowest overall risk score. "
        )
    else:
        explanation += (
            f"Route {safest['route_id']} has the "
            f"lowest overall risk score of "
            f"{safest['risk_score']:.3f}, compared "
            f"with {recommended['risk_score']:.3f} "
            f"for the recommended route. "
        )

    # Final explanation
    explanation += (
        "Considering the assigned cost, time and risk "
        "priorities, the recommended route provides "
        "the best overall trade-off among the "
        "available alternatives."
    )

    # Step 5: Store the result
    results.append({

        "shipment_id": shipment_id,

        "recommended_route": recommended["route_id"],

        "recommended_cost": recommended["cost"],

        "recommended_transit_days":
            recommended["transit_days"],

        "recommended_risk_score":
            recommended["risk_score"],

        "weighted_score":
            recommended["weighted_score"],

        "cheapest_route": cheapest["route_id"],

        "fastest_route": fastest["route_id"],

        "lowest_risk_route": safest["route_id"],

        "recommendation_explanation": explanation

    })


# Step 6: Convert results into DataFrame
explanation_df = pd.DataFrame(results)


# Step 7: Display explanations
print("\nEXPLAINABLE ROUTE RECOMMENDATIONS:\n")

for _, row in explanation_df.head(5).iterrows():

    print("Shipment:", row["shipment_id"])

    print("Recommended Route:",
          row["recommended_route"])

    print("Cheapest Route:",
          row["cheapest_route"])

    print("Fastest Route:",
          row["fastest_route"])

    print("Lowest Risk Route:",
          row["lowest_risk_route"])

    print("Explanation:")

    print(row["recommendation_explanation"])

    print("-" * 70)


# Step 8: Save explanation results
explanation_df.to_csv(
    "data/explainable_recommendations.csv",
    index=False
)


print("\nEXPLANATIONS GENERATED SUCCESSFULLY!")

print("Total shipments explained:",
      len(explanation_df))

print("\nSaved file:")
print("data/explainable_recommendations.csv")
