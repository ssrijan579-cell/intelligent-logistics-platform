"""
Train Random Forest model for logistics delivery delay prediction.
"""

# ==========================================================
# Imports
# ==========================================================

import warnings

import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)

from sklearn.model_selection import train_test_split

from sklearn.pipeline import Pipeline

from sklearn.preprocessing import (
    OneHotEncoder,
    StandardScaler,
)

warnings.filterwarnings("ignore")

# ==========================================================
# Load Dataset
# ==========================================================

DATA_PATH = "ml/data/processed/logistics_shipments_processed.csv"

df = pd.read_csv(DATA_PATH)

print("=" * 60)
print("DATASET LOADED")
print("=" * 60)

print(f"\nDataset Shape : {df.shape}")

print("\nColumns")

print(df.columns.tolist())

# ==========================================================
# Feature Engineering
# ==========================================================

# Convert datetime columns

datetime_columns = [
    "booking_datetime",
    "dispatch_datetime",
    "expected_delivery_datetime",
    "actual_delivery_datetime",
]

for col in datetime_columns:
    df[col] = pd.to_datetime(df[col])

# Extract booking features

df["booking_month"] = df["booking_datetime"].dt.month

df["booking_day"] = df["booking_datetime"].dt.day

df["booking_weekday"] = df["booking_datetime"].dt.weekday

df["booking_hour"] = df["booking_datetime"].dt.hour

print("\nFeature engineering completed.")

# ==========================================================
# Feature Selection
# ==========================================================

target = "delayed"

features = [
    "origin_city",
    "destination_city",
    "distance_km",
    "package_type",
    "vehicle_type",
    "vehicle_speed_kmph",
    "shipment_weight_kg",
    "weather",
    "traffic_level",
    "route_type",
    "driver_experience_years",
    "warehouse_load",
    "customer_priority",
    "fuel_price_per_litre",
    "fuel_consumption_litres",
    "expected_travel_hours",
    "delivery_cost",
    "is_weekend",
    "is_holiday",
    "booking_month",
    "booking_day",
    "booking_weekday",
    "booking_hour",
]

X = df[features]

y = df[target]

print("\nFeature matrix shape :", X.shape)
print("Target shape :", y.shape)

# ==========================================================
# Train-Test Split
# ==========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y,
)

print("\nTraining samples :", len(X_train))
print("Testing samples  :", len(X_test))

# ==========================================================
# Numerical & Categorical Features
# ==========================================================

numerical_features = [
    "distance_km",
    "vehicle_speed_kmph",
    "shipment_weight_kg",
    "driver_experience_years",
    "fuel_price_per_litre",
    "fuel_consumption_litres",
    "expected_travel_hours",
    "delivery_cost",
    "booking_month",
    "booking_day",
    "booking_weekday",
    "booking_hour",
]

categorical_features = [
    "origin_city",
    "destination_city",
    "package_type",
    "vehicle_type",
    "weather",
    "traffic_level",
    "route_type",
    "warehouse_load",
    "customer_priority",
    "is_weekend",
    "is_holiday",
]

# ==========================================================
# Preprocessing Pipeline
# ==========================================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "num",
            StandardScaler(),
            numerical_features,
        ),
        (
            "cat",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features,
        ),
    ]
)

print("\nPreprocessing pipeline created successfully.")

# ==========================================================
# Build Random Forest Pipeline
# ==========================================================

model = Pipeline(
    steps=[
        (
            "preprocessor",
            preprocessor,
        ),
        (
            "classifier",
            RandomForestClassifier(
                n_estimators=300,
                max_depth=15,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1,
            ),
        ),
    ]
)

print("\n" + "=" * 60)
print("Training Random Forest Model...")
print("=" * 60)

model.fit(
    X_train,
    y_train,
)

print("Random Forest training completed!")

# ==========================================================
# Predictions
# ==========================================================

y_pred = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    y_pred,
)

print("\nAccuracy")
print("-" * 30)
print(f"{accuracy:.4f}")

print("\nClassification Report")
print("-" * 30)

print(
    classification_report(
        y_test,
        y_pred,
    )
)

print("\nConfusion Matrix")
print("-" * 30)

print(
    confusion_matrix(
        y_test,
        y_pred,
    )
)

# ==========================================================
# Feature Importance
# ==========================================================

feature_names = model.named_steps[
    "preprocessor"
].get_feature_names_out()

importances = model.named_steps[
    "classifier"
].feature_importances_

importance_df = (
    pd.DataFrame(
        {
            "Feature": feature_names,
            "Importance": importances,
        }
    )
    .sort_values(
        by="Importance",
        ascending=False,
    )
)

print("\nTop 20 Feature Importances")
print("-" * 30)

print(
    importance_df.head(20).to_string(index=False)
)

# ==========================================================
# Save Model
# ==========================================================

import os

MODEL_DIR = "ml/models"

os.makedirs(
    MODEL_DIR,
    exist_ok=True,
)

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "random_forest_model.pkl",
)

joblib.dump(
    model,
    MODEL_PATH,
)

print("\nRandom Forest model saved successfully!")

print(f"\nModel Path : {MODEL_PATH}")

# ==========================================================
# Save Feature Importance
# ==========================================================

FEATURE_PATH = os.path.join(
    MODEL_DIR,
    "feature_importance.csv",
)

importance_df.to_csv(
    FEATURE_PATH,
    index=False,
)

print(f"Feature Importance saved to : {FEATURE_PATH}")

# ==========================================================
# Training Summary
# ==========================================================

print("\n" + "=" * 60)
print("MODEL TRAINING COMPLETED SUCCESSFULLY")
print("=" * 60)

print(f"Training Samples : {len(X_train)}")
print(f"Testing Samples  : {len(X_test)}")
print(f"Accuracy         : {accuracy:.4f}")

print("\nTop 10 Important Features")

print(
    importance_df.head(10).to_string(
        index=False
    )
)

print("\nSaved Files")

print(f"1. {MODEL_PATH}")
print(f"2. {FEATURE_PATH}")

print("\nSprint 3 Completed Successfully!")