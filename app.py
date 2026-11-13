
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# --------------------------------
# PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="Shipment Route Optimizer",
    page_icon="🚚",
    layout="wide"
)

# --------------------------------
# LOAD DATASET
# --------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "normalized_routes.csv"


@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)


try:
    df = load_data()
except Exception as e:
    st.error(f"Unable to load dataset: {e}")
    st.stop()


# Check required columns
required_columns = [
    "shipment_id",
    "origin",
    "destination",
    "route_id",
    "intermediate_hub",
    "cost",
    "transit_days",
    "risk_score",
    "cost_norm",
    "time_norm",
    "risk_norm"
]

if not all(col in df.columns for col in required_columns):
    st.error("Required dataset columns are missing.")
    st.stop()


# --------------------------------
# DASHBOARD HEADER
# --------------------------------

st.title("🚚 Shipment Route Optimizer")

st.markdown(
    "### Intelligent Shipment Route Recommendation System"
)

st.write(
    "Optimize shipment routes based on transportation "
    "cost, transit time and operational risk."
)

st.divider()


# --------------------------------
# DASHBOARD OVERVIEW
# --------------------------------

total_shipments = df["shipment_id"].nunique()
total_routes = len(df)

avg_cost = df["cost"].mean()
avg_time = df["transit_days"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Shipments", total_shipments)

col2.metric("Available Routes", total_routes)

col3.metric("Average Cost", f"₹{avg_cost:,.0f}")

col4.metric("Average Transit Time", f"{avg_time:.1f} days")

st.divider()


# --------------------------------
# SHIPMENT SELECTION
# --------------------------------

st.subheader("📦 Select Shipment")

shipment_ids = sorted(df["shipment_id"].unique())

selected_shipment = st.selectbox(
    "Choose Shipment ID",
    shipment_ids
)

shipment_df = df[
    df["shipment_id"] == selected_shipment
].copy()


# --------------------------------
# WEIGHT ADJUSTMENT
# --------------------------------

st.subheader("⚖️ Optimization Preferences")

st.write(
    "Adjust the importance of cost, transit time and risk."
)

col1, col2, col3 = st.columns(3)

with col1:
    cost_weight = st.slider(
        "Cost Importance (%)",
        0, 100, 40
    )

with col2:
    time_weight = st.slider(
        "Time Importance (%)",
        0, 100, 30
    )

with col3:
    risk_weight = st.slider(
        "Risk Importance (%)",
        0, 100, 30
    )


# Convert weights into proportions
total_weight = cost_weight + time_weight + risk_weight

if total_weight == 0:

    st.warning(
        "All weights are zero. Equal weights will be used."
    )

    cost_weight = 1
    time_weight = 1
    risk_weight = 1

    total_weight = 3


cost_weight = cost_weight / total_weight
time_weight = time_weight / total_weight
risk_weight = risk_weight / total_weight


# --------------------------------
# CALCULATE WEIGHTED SCORE
# --------------------------------

shipment_df["weighted_score"] = (

    cost_weight * shipment_df["cost_norm"] +

    time_weight * shipment_df["time_norm"] +

    risk_weight * shipment_df["risk_norm"]

)


# Sort routes
shipment_df = shipment_df.sort_values(
    by="weighted_score",
    ascending=True
).reset_index(drop=True)


# Select best route
best_route = shipment_df.iloc[0]

top_three = shipment_df.head(3)


# --------------------------------
# RECOMMENDED ROUTE
# --------------------------------

st.divider()

st.subheader("🏆 Best Route Recommendation")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Recommended Route",
    best_route["route_id"]
)

col2.metric(
    "Intermediate Hub",
    best_route["intermediate_hub"]
)

col3.metric(
    "Transportation Cost",
    f"₹{best_route['cost']:,.0f}"
)

col4.metric(
    "Transit Time",
    f"{int(best_route['transit_days'])} days"
)

st.success(
    f"Recommended Route: {best_route['route_id']} "
    f"with weighted score "
    f"{best_route['weighted_score']:.4f}"
)


# --------------------------------
# ROUTE COMPARISON
# --------------------------------

st.divider()

st.subheader("📊 Top 3 Route Comparison")

display_df = top_three[[
    "route_id",
    "intermediate_hub",
    "cost",
    "transit_days",
    "risk_score",
    "weighted_score"
]].copy()

display_df.columns = [
    "Route",
    "Intermediate Hub",
    "Cost (₹)",
    "Transit Days",
    "Risk Score",
    "Weighted Score"
]

st.dataframe(
    display_df,
    width="stretch",
    hide_index=True
)


# --------------------------------
# ROUTE SCORE CHART
# --------------------------------

st.subheader("📈 Weighted Score Comparison")

fig = px.bar(
    shipment_df,
    x="route_id",
    y="weighted_score",
    color="route_id",
    text="weighted_score",
    title="Weighted Score of Available Routes",
    labels={
        "route_id": "Route",
        "weighted_score": "Weighted Score"
    }
)

fig.update_traces(
    texttemplate="%{text:.3f}",
    textposition="outside"
)

fig.update_layout(
    showlegend=False
)

st.plotly_chart(
    fig,
    width="stretch"
)


# --------------------------------
# CHEAPEST, FASTEST AND LOWEST RISK
# --------------------------------

st.divider()

st.subheader("🔍 Route Analysis")

cheapest = shipment_df.loc[
    shipment_df["cost"].idxmin()
]

fastest = shipment_df.loc[
    shipment_df["transit_days"].idxmin()
]

safest = shipment_df.loc[
    shipment_df["risk_score"].idxmin()
]

col1, col2, col3 = st.columns(3)

col1.metric(
    "Cheapest Route",
    cheapest["route_id"],
    f"₹{cheapest['cost']:,.0f}"
)

col2.metric(
    "Fastest Route",
    fastest["route_id"],
    f"{int(fastest['transit_days'])} days"
)

col3.metric(
    "Lowest Risk Route",
    safest["route_id"],
    f"{safest['risk_score']:.3f}"
)


# --------------------------------
# EXPLANATION
# --------------------------------

st.divider()

st.subheader("💡 Explainable Recommendation")

explanation = (
    f"Route {best_route['route_id']} is recommended "
    f"for shipment {selected_shipment} because it has "
    f"the lowest weighted score of "
    f"{best_route['weighted_score']:.4f}. "
)

if cheapest["route_id"] == best_route["route_id"]:

    explanation += "It is also the cheapest available route. "

else:

    explanation += (
        f"The cheapest route is {cheapest['route_id']} "
        f"at ₹{cheapest['cost']:,.0f}. "
    )


if fastest["route_id"] == best_route["route_id"]:

    explanation += "It is also the fastest available route. "

else:

    explanation += (
        f"The fastest route is {fastest['route_id']} "
        f"with {int(fastest['transit_days'])} days of transit. "
    )


if safest["route_id"] == best_route["route_id"]:

    explanation += "It also has the lowest overall risk. "

else:

    explanation += (
        f"The lowest-risk route is {safest['route_id']} "
        f"with a risk score of {safest['risk_score']:.3f}. "
    )


explanation += (
    "Based on the selected cost, time and risk preferences, "
    "this route provides the best overall trade-off."
)

st.info(explanation)


# --------------------------------
# COMPLETE ROUTE DETAILS
# --------------------------------

st.divider()

st.subheader("📋 All Available Routes")

st.dataframe(
    shipment_df[[
        "route_id",
        "intermediate_hub",
        "cost",
        "transit_days",
        "delay_probability",
        "congestion_risk",
        "geopolitical_risk",
        "risk_score",
        "weighted_score"
    ]],
    width="stretch",
    hide_index=True
)


# --------------------------------
# FOOTER
# --------------------------------

st.divider()

st.caption(
    "Shipment Route Optimizer | "
    "Powered by Python, Streamlit, Pandas and Plotly"
)
