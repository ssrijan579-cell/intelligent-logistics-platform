import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)

from sklearn.ensemble import RandomForestClassifier

from xgboost import XGBClassifier

DATA_PATH = "ml/data/raw/logistics_shipments.csv"

df = pd.read_csv(DATA_PATH)

date_columns = [
    "booking_datetime",
    "dispatch_datetime",
    "expected_delivery_datetime",
    "actual_delivery_datetime",
]

for col in date_columns:
    df[col] = pd.to_datetime(df[col])

df["booking_hour"] = df["booking_datetime"].dt.hour
df["booking_day"] = df["booking_datetime"].dt.day
df["booking_month"] = df["booking_datetime"].dt.month
df["booking_weekday"] = df["booking_datetime"].dt.weekday


X = df.drop(
    columns=[
        "shipment_id",
        "booking_datetime",
        "dispatch_datetime",
        "expected_delivery_datetime",
        "actual_delivery_datetime",
        "delay_minutes",      # Remove leakage
        "delayed",
    ]
)
y = df["delayed"]


preprocessor = joblib.load(
    "ml/models/preprocessor.pkl"
)


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y,
)

X_train = preprocessor.transform(X_train)
X_test = preprocessor.transform(X_test)

# ----------------------------------------------------
# Train Random Forest Model
# ----------------------------------------------------

print("\n" + "=" * 60)
print("Training Random Forest Model...")
print("=" * 60)

rf_model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    random_state=42,
    n_jobs=-1,
)

rf_model.fit(X_train, y_train)

print("Random Forest training completed!")

# ----------------------------------------------------
# Predictions
# ----------------------------------------------------

y_pred = rf_model.predict(X_test)

# ----------------------------------------------------
# Evaluation
# ----------------------------------------------------

accuracy = accuracy_score(y_test, y_pred)

print("\nAccuracy")
print("-" * 30)
print(f"{accuracy:.4f}")

print("\nClassification Report")
print("-" * 30)
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix")
print("-" * 30)
print(confusion_matrix(y_test, y_pred))

# ----------------------------------------------------
# Feature Importance
# ----------------------------------------------------

print("\nTop Feature Importances")

feature_names = preprocessor.get_feature_names_out()

importance_df = pd.DataFrame(
    {
        "Feature": feature_names,
        "Importance": rf_model.feature_importances_,
    }
)

importance_df = importance_df.sort_values(
    by="Importance",
    ascending=False,
)

print(importance_df.head(15).to_string(index=False))

# ----------------------------------------------------
# Save Model
# ----------------------------------------------------

joblib.dump(
    rf_model,
    "ml/models/random_forest.pkl",
)

print("\nRandom Forest model saved successfully!")

print("=" * 60)