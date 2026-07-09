import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (
    OneHotEncoder,
    StandardScaler,
)

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

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)


X_train_processed = preprocessor.fit_transform(X_train)
X_test_processed = preprocessor.transform(X_test)


joblib.dump(
    preprocessor,
    "ml/models/preprocessor.pkl",
)

print("Preprocessor saved successfully!")