import requests

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