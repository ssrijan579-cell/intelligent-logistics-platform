import streamlit as st

st.set_page_config(
    page_title="About Project",
    page_icon="ℹ️",
    layout="wide",
)

st.title("🚚 Intelligent Logistics Platform")

st.markdown("---")

st.header("Project Overview")

st.write("""
The Intelligent Logistics Platform is an end-to-end Machine Learning project
that predicts shipment delays before dispatch.

The system not only predicts whether a shipment will be delayed,
but also estimates the delay duration, identifies the probable
root causes, and recommends operational improvements.

The project demonstrates a complete ML lifecycle including:

- Synthetic Data Generation
- Feature Engineering
- Classification
- Regression
- Explainability
- Recommendation Engine
- FastAPI Deployment
- Streamlit Dashboard
""")

st.markdown("---")

st.header("Technology Stack")

col1, col2 = st.columns(2)

with col1:

    st.subheader("Machine Learning")

    st.write("""
- Python
- Scikit-Learn
- CatBoost
- Random Forest
- XGBoost
- LightGBM
- Pandas
- NumPy
""")

with col2:

    st.subheader("Deployment")

    st.write("""
- FastAPI
- Streamlit
- Pydantic
- Joblib
- Plotly
- Requests
""")

st.markdown("---")

st.header("Project Architecture")

st.code(
"""
Synthetic Dataset
        │
        ▼
Feature Engineering
        │
        ▼
Classification Model
(Random Forest)
        │
        ▼
Regression Model
(CatBoost)
        │
        ▼
Root Cause Analysis
        │
        ▼
Recommendation Engine
        │
        ▼
FastAPI
        │
        ▼
Streamlit Dashboard
"""
)

st.markdown("---")

st.header("Machine Learning Models")

st.table(
{
    "Task":[
        "Delay Prediction",
        "Delay Estimation",
    ],
    "Best Model":[
        "Random Forest",
        "CatBoost",
    ]
}
)

st.markdown("---")

st.header("Project Features")

features = [

    "✅ Shipment Delay Prediction",

    "✅ Delay Time Estimation",

    "✅ Root Cause Analysis",

    "✅ Operational Recommendations",

    "✅ REST API using FastAPI",

    "✅ Interactive Streamlit Dashboard",

    "✅ Model Analytics",

    "✅ Dataset Explorer",

]

for feature in features:
    st.write(feature)

st.markdown("---")

st.header("Performance")

metric1, metric2, metric3 = st.columns(3)

with metric1:
    st.metric(
        "Classification Accuracy",
        "97%"
    )

with metric2:
    st.metric(
        "Regression R²",
        "0.72"
    )

with metric3:
    st.metric(
        "Models",
        "6"
    )

st.markdown("---")

st.header("Developer")

st.write("**Srijan Srivastava**")

st.write("B.Tech Information Technology")

st.write("Machine Learning | Data Science | AI")

st.markdown("---")

st.success(
"""
This project demonstrates an end-to-end production-ready
Machine Learning workflow including data generation,
model training, deployment, explainability,
and interactive visualization.
"""
)