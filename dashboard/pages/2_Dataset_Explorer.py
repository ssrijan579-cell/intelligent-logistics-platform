import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Dataset Explorer",
    page_icon="📁",
    layout="wide",
)

st.title("📁 Dataset Explorer")

try:
    df = pd.read_csv("ml/data/processed/logistics_shipments_processed.csv")
except FileNotFoundError:
    st.error("Dataset not found.")
    st.stop()

st.metric("Total Shipments", len(df))
st.metric("Total Features", len(df.columns))

st.markdown("---")

st.subheader("Search Shipments")

search = st.text_input("Search Shipment ID")

if search:
    filtered = df[df["shipment_id"].str.contains(search, case=False)]
else:
    filtered = df

st.dataframe(filtered, use_container_width=True)

st.markdown("---")

st.subheader("Filter by Weather")

weather = st.selectbox(
    "Weather",
    ["All"] + sorted(df["weather"].unique().tolist())
)

if weather != "All":
    filtered = filtered[filtered["weather"] == weather]

st.dataframe(filtered, use_container_width=True)

st.download_button(
    "⬇ Download CSV",
    filtered.to_csv(index=False),
    file_name="filtered_shipments.csv",
    mime="text/csv",
)