import os

import requests
import streamlit as st

API_URL = "https://intelligent-logistics-platform.onrender.com/predict"


def predict_shipment(data):

    try:

        response = requests.post(
            API_URL,
            json=data,
            timeout=120,
        )

        if response.status_code == 200:
            return response.json()

        return {
            "error": response.text
        }

    except Exception as e:

        return {
            "error": str(e)
        }

# =====================================================
# Customer Feedback API
# =====================================================

try:
    FEEDBACK_API_BASE_URL = st.secrets["FEEDBACK_API_BASE_URL"].rstrip("/")
except Exception:
    FEEDBACK_API_BASE_URL = os.getenv(
        "FEEDBACK_API_BASE_URL",
        "http://127.0.0.1:8000"
    ).rstrip("/")

def submit_feedback(data):
    response = requests.post(
        f"{FEEDBACK_API_BASE_URL}/feedback",
        json=data,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def get_feedback_records(admin_key, limit=100, offset=0):
    response = requests.get(
        f"{FEEDBACK_API_BASE_URL}/feedback/admin",
        headers={"X-Admin-API-Key": admin_key},
        params={"limit": limit, "offset": offset},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def get_feedback_summary(admin_key):
    response = requests.get(
        f"{FEEDBACK_API_BASE_URL}/feedback/admin/summary",
        headers={"X-Admin-API-Key": admin_key},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
