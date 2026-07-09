"""
Train Regression Models
Predict Delay Minutes
"""

import pandas as pd
import joblib

# ==========================================================
# Load Dataset
# ==========================================================

df = pd.read_csv(
    "ml/data/processed/logistics_shipments_processed.csv"
)

print("=" * 70)
print("DATASET INFORMATION")
print("=" * 70)

print("\nShape")
print(df.shape)

print("\nColumns")
print(df.columns.tolist())

print("\nFirst Five Rows")
print(df.head())

print("\nTarget Statistics")
print(df["delay_minutes"].describe())

# ==========================================================
# Define Features and Target
# ==========================================================

# Target variable
y = df["delay_minutes"]

# Columns to remove
drop_columns = [

    "shipment_id",

    "booking_datetime",

    "dispatch_datetime",

    "expected_delivery_datetime",

    "actual_delivery_datetime",

    "delay_minutes",

    "delayed",

]

# Features
X = df.drop(columns=drop_columns)

print("\nFeatures used for training:\n")

print(X.columns.tolist())

print(f"\nTotal Features: {len(X.columns)}")

print("\nTarget Summary\n")

print(y.describe())

# ==========================================================
# Separate Numerical & Categorical Features
# ==========================================================

categorical_features = X.select_dtypes(
    include=["object"]
).columns.tolist()

numerical_features = X.select_dtypes(
    exclude=["object"]
).columns.tolist()

print("\nCategorical Features")
print(categorical_features)

print("\nNumerical Features")
print(numerical_features)


# ==========================================================
# Preprocessing Pipeline
# ==========================================================

from sklearn.compose import ColumnTransformer

from sklearn.preprocessing import (
    OneHotEncoder,
    StandardScaler,
)

preprocessor = ColumnTransformer(

    transformers=[

        (
            "cat",
            OneHotEncoder(
                handle_unknown="ignore",
            ),
            categorical_features,
        ),

        (
            "num",
            StandardScaler(),
            numerical_features,
        ),
    ]
)

print("\nPreprocessor Created Successfully")

# ==========================================================
# Train Test Split
# ==========================================================

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.20,

    random_state=42,

)

print("\nTrain-Test Split Completed")

print(f"\nTraining Samples : {len(X_train)}")

print(f"Testing Samples  : {len(X_test)}")

print(f"\nX_train Shape : {X_train.shape}")

print(f"X_test Shape  : {X_test.shape}")

print(f"\ny_train Shape : {y_train.shape}")

print(f"y_test Shape  : {y_test.shape}")

# ==========================================================
# Regression Models
# ==========================================================

from sklearn.pipeline import Pipeline

from sklearn.linear_model import LinearRegression

from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor,
)

from xgboost import XGBRegressor

from lightgbm import LGBMRegressor

from catboost import CatBoostRegressor

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

import pandas as pd
import numpy as np


# ==========================================================
# Models
# ==========================================================

models = {

    "Linear Regression": LinearRegression(),

    "Random Forest": RandomForestRegressor(
        n_estimators=200,
        random_state=42,
    ),

    "Gradient Boosting": GradientBoostingRegressor(
        random_state=42,
    ),

    "XGBoost": XGBRegressor(
        random_state=42,
        objective="reg:squarederror",
    ),

    "LightGBM": LGBMRegressor(
        random_state=42,
    ),

    "CatBoost": CatBoostRegressor(
        verbose=0,
        random_state=42,
    ),

}


results = []
trained_pipelines = {}


# ==========================================================
# Train Models
# ==========================================================

for name, model in models.items():

    print("\n" + "=" * 60)
    print(f"Training {name}...")
    print("=" * 60)

    pipeline = Pipeline(

        steps=[

            ("preprocessor", preprocessor),

            ("model", model),

        ]
    )

    pipeline.fit(
        X_train,
        y_train,
    )
    trained_pipelines[name] = pipeline

    predictions = pipeline.predict(
        X_test
    )

    mae = mean_absolute_error(
        y_test,
        predictions,
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_test,
            predictions,
        )
    )

    r2 = r2_score(
        y_test,
        predictions,
    )

    print(f"MAE  : {mae:.2f}")
    print(f"RMSE : {rmse:.2f}")
    print(f"R²   : {r2:.4f}")

    results.append({

        "Model": name,

        "MAE": mae,

        "RMSE": rmse,

        "R2 Score": r2,

    })


# ==========================================================
# Model Comparison
# ==========================================================

results_df = pd.DataFrame(results)

results_df = results_df.sort_values(
    by="R2 Score",
    ascending=False,
)

print("\n")
print("=" * 80)
print("REGRESSION MODEL COMPARISON")
print("=" * 80)

print(results_df)

print("=" * 80)


# ==========================================================
# Save Results
# ==========================================================

results_df.to_csv(
    "ml/models/regression_results.csv",
    index=False,
)

print("\nResults saved successfully.")


# ==========================================================
# Best Model
# ==========================================================

best = results_df.iloc[0]
best_pipeline = trained_pipelines[best["Model"]]
joblib.dump(
    best_pipeline,
    "ml/models/delay_regression_model.pkl"
)

print("\nRegression model saved successfully.")

print("\n")
print("=" * 80)
print("BEST REGRESSION MODEL")
print("=" * 80)

print(best)



