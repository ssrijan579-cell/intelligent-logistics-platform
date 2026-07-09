"""
Compare multiple machine learning models.
"""

import warnings
import joblib
warnings.filterwarnings("ignore")

import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.compose import ColumnTransformer

from sklearn.pipeline import Pipeline

from sklearn.preprocessing import (
    StandardScaler,
    OneHotEncoder,
)

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)

# Models
from sklearn.linear_model import LogisticRegression

from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier,
)

from xgboost import XGBClassifier

from lightgbm import LGBMClassifier

from catboost import CatBoostClassifier

# -------------------------------------------------------
# Load Dataset
# -------------------------------------------------------

df = pd.read_csv(
    "ml/data/processed/logistics_shipments_processed.csv"
)

print(df.shape)
print(df.head())

target = "delayed"

leakage_columns = [
    "shipment_id",
    "booking_datetime",
    "dispatch_datetime",
    "expected_delivery_datetime",
    "actual_delivery_datetime",
    "delay_minutes",
    "delayed",
]

X = df.drop(columns=leakage_columns)

y = df[target]

print("\nFeatures used for training:\n")
print(X.columns.tolist())
print(f"\nTotal Features: {len(X.columns)}")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)

categorical_features = X.select_dtypes(
    include="object"
).columns.tolist()

numerical_features = X.select_dtypes(
    exclude="object"
).columns.tolist()


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

# -------------------------------------------------------
# Models
# -------------------------------------------------------

models = {
    "Logistic Regression": LogisticRegression(
        max_iter=1000,
        random_state=42,
    ),

    "Random Forest": RandomForestClassifier(
        n_estimators=300,
        random_state=42,
    ),

    "Gradient Boosting": GradientBoostingClassifier(
        random_state=42,
    ),

    "XGBoost": XGBClassifier(
        random_state=42,
        eval_metric="logloss",
        use_label_encoder=False,
    ),

    "LightGBM": LGBMClassifier(
        random_state=42,
        verbose=-1,
    ),

    "CatBoost": CatBoostClassifier(
        random_state=42,
        verbose=False,
    ),
}

# -------------------------------------------------------
# Store Results
# -------------------------------------------------------

results = []

# -------------------------------------------------------
# Train & Evaluate
# -------------------------------------------------------

best_pipeline = None
best_f1 = -1

for name, model in models.items():

    print("\n" + "=" * 60)
    print(f"Training {name}...")
    print("=" * 60)

    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", model),
    ])

    pipeline.fit(X_train, y_train)

    predictions = pipeline.predict(X_test)
    probabilities = pipeline.predict_proba(X_test)[:, 1]

    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions)
    recall = recall_score(y_test, predictions)
    f1 = f1_score(y_test, predictions)
    roc_auc = roc_auc_score(y_test, probabilities)

    if f1 > best_f1:
        best_f1 = f1
        best_pipeline = pipeline

    results.append({
        "Model": name,
        "Accuracy": round(accuracy, 4),
        "Precision": round(precision, 4),
        "Recall": round(recall, 4),
        "F1 Score": round(f1, 4),
        "ROC AUC": round(roc_auc, 4),
    })

    print(f"Accuracy : {accuracy:.4f}")
    print(f"F1 Score : {f1:.4f}")

    # -------------------------------------------------------
# Results DataFrame
# -------------------------------------------------------

results_df = pd.DataFrame(results)

results_df = results_df.sort_values(
    by="F1 Score",
    ascending=False,
)

print("\n")
print("=" * 80)
print("MODEL COMPARISON")
print("=" * 80)

print(results_df)

print("=" * 80)

# -------------------------------------------------------
# Save Results
# -------------------------------------------------------

results_df.to_csv(
    "ml/models/model_comparison_results.csv",
    index=False,
)

print("\nResults saved successfully.")

# -------------------------------------------------------
# Best Model
# -------------------------------------------------------

best_model = results_df.iloc[0]

print("\n")
print("=" * 80)
print("BEST MODEL")
print("=" * 80)

print(best_model)

# -------------------------------------------------------
# Save Best Model
# -------------------------------------------------------

joblib.dump(
    best_pipeline,
    "ml/models/best_model.pkl",
)

print("\nBest model saved to ml/models/best_model.pkl")