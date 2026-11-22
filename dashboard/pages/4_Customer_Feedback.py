import streamlit as st
import requests
from api import submit_feedback, get_feedback_api_status

st.set_page_config(
    page_title="Customer Feedback",
    page_icon="⭐",
    layout="wide",
)

st.title("⭐ Customer Feedback Portal")
st.caption("Help us improve your shipment delivery experience.")

st.markdown("---")

st.subheader("Share Your Experience")

st.write(
    "Enter your shipment ID and rate the different aspects "
    "of your delivery."
)

with st.form("customer_feedback_form"):

    shipment_id = st.text_input(
        "Shipment ID",
        placeholder="Example: SHP0000002",
        max_chars=10,
    )

    st.markdown("### Rate Your Experience")

    overall_rating = st.slider(
        "Overall Experience",
        min_value=1,
        max_value=5,
        value=5,
    )

    col1, col2 = st.columns(2)

    with col1:
        delivery_rating = st.slider(
            "Delivery Experience",
            min_value=1,
            max_value=5,
            value=5,
        )

        agent_rating = st.slider(
            "Delivery Agent",
            min_value=1,
            max_value=5,
            value=5,
        )

    with col2:
        packaging_rating = st.slider(
            "Packaging Quality",
            min_value=1,
            max_value=5,
            value=5,
        )

    comments = st.text_area(
        "Your Feedback",
        placeholder="Tell us about your delivery experience...",
        max_chars=2000,
    )

    submitted = st.form_submit_button(
        "Submit Feedback",
        type="primary",
        use_container_width=True,
    )

if submitted:

    shipment_id = shipment_id.strip().upper()
    comments = comments.strip()

    if not shipment_id:
        st.error("Please enter your shipment ID.")

    elif len(comments) < 5:
        st.error("Please enter at least 5 characters of feedback.")

    else:
        feedback_data = {
            "shipment_id": shipment_id,
            "overall_rating": overall_rating,
            "delivery_rating": delivery_rating,
            "agent_rating": agent_rating,
            "packaging_rating": packaging_rating,
            "comments": comments,
        }

        try:
            result = submit_feedback(feedback_data)

            st.success("Thank you! Your feedback was submitted successfully.")

            st.write(
                f"Feedback Reference: {result['feedback_id']}"
            )

        except requests.HTTPError as error:

            status_code = (
                error.response.status_code
                if error.response is not None
                else None
            )

            if status_code == 404:
                st.error("Shipment ID was not found.")

            elif status_code == 409:
                st.warning(
                    "Feedback has already been submitted for this shipment."
                )

            elif status_code == 422:
                st.error(
                    "Some submitted information is invalid. Please check your entries."
                )

            else:
                st.error(f"Feedback submission failed: {error}")

        except requests.RequestException as error:
            st.error(
                "Cannot connect to the feedback server. "
                "Please try again later."
            )
            st.caption(str(error))

from api import get_feedback_api_status

st.write("Feedback API configuration:", get_feedback_api_status())
st.write("DEBUG — Feedback API:", get_feedback_api_status())