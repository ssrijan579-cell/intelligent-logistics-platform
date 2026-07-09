import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Model Analytics",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Model Analytics Dashboard")

st.markdown("---")

# ==========================================
# Load Model Comparison Results
# ==========================================

try:

    df = pd.read_csv(
        "ml/models/model_comparison_results.csv"
    )

except:

    st.error(
        "model_comparison_results.csv not found."
    )

    st.stop()

# ==========================================
# Display Table
# ==========================================

st.subheader("Model Comparison")

st.dataframe(
    df,
    use_container_width=True,
)

# ==========================================
# Accuracy Chart
# ==========================================

st.subheader("Accuracy Comparison")

fig = px.bar(
    df,
    x="Model",
    y="Accuracy",
    text="Accuracy",
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

# ==========================================
# F1 Score Chart
# ==========================================

st.subheader("F1 Score Comparison")

fig = px.bar(
    df,
    x="Model",
    y="F1 Score",
    text="F1 Score",
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

# ==========================================
# ROC AUC
# ==========================================

st.subheader("ROC AUC Comparison")

fig = px.bar(
    df,
    x="Model",
    y="ROC AUC",
    text="ROC AUC",
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

# ==========================================
# Best Model
# ==========================================

best = df.iloc[0]

st.success(
    f"""
Best Model

🏆 {best['Model']}

Accuracy : {best['Accuracy']:.3f}

F1 Score : {best['F1 Score']:.3f}

ROC AUC : {best['ROC AUC']:.3f}
"""
)