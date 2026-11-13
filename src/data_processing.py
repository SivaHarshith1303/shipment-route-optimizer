
import pandas as pd

# Load the dataset
df = pd.read_csv("data/shipment_routes.csv")


# Display dataset information
print("DATASET LOADED SUCCESSFULLY")

print("\nFirst 5 records:")
print(df.head())


# Check dataset shape
print("\nDataset Shape:")
print(df.shape)


# Check column names
print("\nColumn Names:")
print(df.columns.tolist())


# Check missing values
print("\nMissing Values:")
print(df.isnull().sum())


# Check duplicate records
print("\nDuplicate Records:")
print(df.duplicated().sum())


# Validate numerical values
print("\nChecking invalid values:")

print("Invalid costs:", (df["cost"] <= 0).sum())

print("Invalid transit days:", (df["transit_days"] <= 0).sum())

print(
    "Invalid delay probabilities:",
    ((df["delay_probability"] < 0) |
     (df["delay_probability"] > 1)).sum()
)


# Check number of shipments
print("\nTotal Shipments:")
print(df["shipment_id"].nunique())


# Check number of routes
print("\nTotal Route Options:")
print(len(df))


# Check routes per shipment
print("\nRoutes per Shipment:")
print(df.groupby("shipment_id").size())


print("\nDATA PREPROCESSING CHECK COMPLETED")
