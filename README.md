
# Shipment Route Optimizer

## 1. Project Overview

The Shipment Route Optimizer is an intelligent route recommendation
system designed to identify the most suitable transportation route
for shipments based on cost, transit time and operational risk.

The system uses weighted scoring and route ranking techniques to
recommend the best available route for each shipment.

## 2. Objectives

- Minimize transportation costs.
- Reduce shipment transit time.
- Consider operational risks.
- Recommend the best route among available alternatives.
- Provide explainable route recommendations.

## 3. Technologies Used

- Programming Language: Python
- Frontend: Streamlit
- Data Processing: Pandas, NumPy
- Data Visualization: Plotly
- Dataset: CSV

## 4. Project Modules

1. Data Processing
2. Data Normalization
3. Weighted Route Scoring
4. Route Recommendation
5. Explainable Recommendation
6. Streamlit Dashboard
7. Testing and Validation

## 5. Algorithm

The system uses weighted scoring to evaluate available routes.

Weighted Score = (0.40 × Cost Score)
               + (0.30 × Time Score)
               + (0.30 × Risk Score)

The route with the lowest weighted score is selected
as the recommended route.

## 6. Project Structure

Shipment_Route_Optimizer/
- data/
- src/
- tests/
- app.py
- requirements.txt
- README.md

## 7. Installation

Install Python and the required dependencies.

Run:

pip install -r requirements.txt

## 8. Execute the Project

Run the data processing modules in sequence:

python src/data_processing.py

python src/normalization.py

python src/route_scoring.py

python src/route_recommendation.py

python src/explanation.py

Start the dashboard:

streamlit run app.py

## 9. Testing

Run automated tests using:

python -m unittest discover -s tests -v

The project includes nine automated validation tests.

## 10. Output

The system generates:

- scored_routes.csv
- recommended_routes.csv
- top3_routes.csv
- explainable_recommendations.csv

## 11. Dashboard Features

- Shipment selection
- Cost, time and risk weight adjustment
- Best route recommendation
- Top three route comparison
- Weighted score visualization
- Explainable recommendations

## 12. Conclusion

The Shipment Route Optimizer provides an intelligent
approach to shipment route selection by considering
transportation cost, transit time and operational risk.

It helps users compare alternative routes and understand
the reasons behind the recommended route.
