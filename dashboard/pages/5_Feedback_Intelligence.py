import os
import requests
import pandas as pd
import streamlit as st

from api import get_feedback_records, get_feedback_summary

st.set_page_config(
    page_title="Feedback Intelligence",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Customer Feedback Intelligence")
st.caption("Administrator dashboard for customer experience monitoring.")

st.markdown("---")

st.subheader("Administrator Authentication")

admin_key = st.text_input(
    "Admin API Key",
    type="password",
    help="Enter the administrator API key configured on the FastAPI server.",
)

if not admin_key:
    st.info("Enter your administrator API key to access feedback analytics.")
    st.stop()

try:
    summary = get_feedback_summary(admin_key)
    result = get_feedback_records(admin_key, limit=500)

except requests.HTTPError as error:

    status_code = (
        error.response.status_code
        if error.response is not None
        else None
    )

    if status_code == 401:
        st.error("Invalid administrator API key.")

    elif status_code == 503:
        st.error("Administrator authentication is not configured on the API.")

    else:
        st.error(f"API request failed: {error}")

    st.stop()

except requests.RequestException as error:
    st.error("Cannot connect to the feedback API.")
    st.caption(str(error))
    st.stop()

st.success("Administrator authenticated successfully.")

st.markdown("---")

st.subheader("Customer Experience Overview")

average_rating = summary.get("average_rating")

try:
    average_rating = float(average_rating or 0)
except (TypeError, ValueError):
    average_rating = 0.0

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Feedback",
    summary.get("total_feedback", 0),
)

col2.metric(
    "Average Rating",
    f"{average_rating:.2f} / 5",
)

col3.metric(
    "Positive Ratings",
    summary.get("positive_ratings", 0),
)

col4.metric(
    "Negative Ratings",
    summary.get("negative_ratings", 0),
)

st.markdown("---")

feedback = result.get("feedback", [])

if not feedback:
    st.info("No customer feedback records are available yet.")

else:
    df = pd.DataFrame(feedback)

    st.subheader("Rating Distribution")

    rating_counts = (
        df["overall_rating"]
        .value_counts()
        .sort_index()
        .reindex([1, 2, 3, 4, 5], fill_value=0)
    )

    st.bar_chart(rating_counts)

    st.markdown("---")

    st.subheader("Customer Feedback Records")

    display_columns = [
        "feedback_id",
        "shipment_id",
        "overall_rating",
        "delivery_rating",
        "agent_rating",
        "packaging_rating",
        "sentiment",
        "complaint_category",
        "created_at",
        "comments",
    ]

    available_columns = [
        column for column in display_columns
        if column in df.columns
    ]

    st.dataframe(
        df[available_columns],
        use_container_width=True,
        hide_index=True,
    )

    st.download_button(
        "Download Feedback CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="customer_feedback.csv",
        mime="text/csv",
    )

st.caption(
    "Sentiment and complaint categories are currently pending NLP analysis."
)
