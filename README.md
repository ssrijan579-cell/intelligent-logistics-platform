# 🚚 Intelligent Delivery Delay Prediction & Logistics Intelligence Platform

An end-to-end **AI-powered logistics intelligence platform** for predicting shipment delays, estimating delivery timelines, explaining model predictions, and providing actionable operational insights through an interactive dashboard.

The platform combines **Machine Learning, Explainable AI, FastAPI, MLflow, data pipelines, model evaluation, and logistics analytics** into a unified system.

## 🚀 Live Demo

🔗 **Dashboard:** [Open Live Dashboard](https://intelligent-logistics-platform-m992dghkqv5wqod6h6zrkv.streamlit.app/)
---

## 🎯 Problem Statement

Delivery delays are a major challenge in logistics operations. Unexpected delays can increase operational costs, affect customer satisfaction, create inefficient resource allocation, and make it difficult for operations teams to prioritize high-risk shipments.

This platform addresses the problem by using machine learning to:

* Predict shipment delay risk
* Estimate delivery timelines
* Identify the factors contributing to predictions
* Analyze logistics performance
* Surface high-risk shipments
* Support data-driven operational decisions

---

## 🚀 Key Features

### 📦 Shipment Delay Prediction

Machine learning models predict the likelihood and severity of shipment delays using shipment, route, operational, and historical features.

### ⏱️ Delivery Time / ETA Prediction

The platform includes regression-based prediction capabilities for estimating delivery time.

### 🔍 Explainable AI

Model predictions are explained using feature importance and SHAP-based explainability techniques to provide insight into the factors influencing delay predictions.

### 📊 Logistics Intelligence Dashboard

An interactive dashboard provides operational analytics and model insights, including:

* Shipment performance
* Delay analysis
* Model analytics
* Dataset exploration
* Feature importance
* Prediction insights

### ⚡ FastAPI Prediction API

A FastAPI-based inference layer exposes the trained machine learning models through structured API endpoints.

### 🧪 MLflow & MLOps

The project incorporates experiment tracking and model lifecycle practices to support reproducible machine learning workflows.

### 🤖 Multiple ML Models

The project evaluates multiple machine learning approaches and stores model comparison and evaluation results.

### 🧬 Reproducible ML Pipeline

The project separates:

* Data generation
* Data processing
* Feature engineering
* Model training
* Model evaluation
* Model inference
* Explainability

### 🧪 Testing

Automated tests are included for validating important prediction and root-cause functionality.

---

## 🏗️ System Architecture

```text
                         Shipment Data
                              │
                              ▼
                      Data Generation
                              │
                              ▼
                       Data Processing
                              │
                              ▼
                     Feature Engineering
                              │
                              ▼
                       Model Training
                              │
                              ▼
                     Model Evaluation
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
             Delay Prediction      ETA Prediction
                    │                   │
                    └─────────┬─────────┘
                              ▼
                     Explainable AI
                    Feature Importance
                         + SHAP
                              │
                              ▼
                       FastAPI API
                              │
                              ▼
                    Prediction Services
                              │
                              ▼
                  Logistics Dashboard
                              │
                              ▼
                  Operational Insights
```

---

## 🧠 Machine Learning Pipeline

The ML pipeline follows an end-to-end workflow:

```text
Data Generation
      ↓
Data Ingestion
      ↓
Data Validation
      ↓
Preprocessing
      ↓
Feature Engineering
      ↓
Train / Validation / Test Split
      ↓
Model Training
      ↓
Model Comparison
      ↓
Model Evaluation
      ↓
Best Model Selection
      ↓
Model Serialization
      ↓
API Inference
      ↓
Dashboard Analytics
```

---

## 📊 Machine Learning

The platform supports both **classification and regression-based prediction workflows**.

### Classification

The classification pipeline is designed to predict shipment delay risk.

Candidate models include:

* Random Forest
* XGBoost
* LightGBM
* CatBoost
* Scikit-learn classification models

### Regression

The regression pipeline estimates shipment delivery time / delay duration.

Models can be compared using:

* MAE
* RMSE
* R²

---

## 🏆 Model Selection

The project includes model comparison artifacts to evaluate different approaches and identify the best-performing model.

Generated model artifacts include:

```text
ml/models/
│
├── best_model.pkl
├── random_forest.pkl
├── random_forest_model.pkl
├── delay_regression_model.pkl
├── preprocessor.pkl
├── model_comparison_results.csv
├── regression_results.csv
└── feature_importance.csv
```

The trained artifacts are used by the inference layer for prediction.

---

## 🔍 Explainable AI

A major component of the platform is model interpretability.

The explainability layer helps answer:

* Why was this shipment predicted to be delayed?
* Which features contributed most to the prediction?
* Which operational factors increase delay risk?
* Which features have the greatest overall influence on the model?

The project includes dedicated explainability components and feature importance artifacts.

---

## 📈 Model Evaluation

The platform evaluates models using task-appropriate metrics.

### Classification Metrics

* Accuracy
* Precision
* Recall
* F1 Score
* ROC-AUC
* Confusion Matrix

### Regression Metrics

* Mean Absolute Error (MAE)
* Root Mean Squared Error (RMSE)
* R² Score

Model comparison results are stored in the `ml/models/` directory.

> Actual benchmark values should be reported directly from the generated evaluation files rather than manually estimated.

---

## 📊 Logistics Intelligence Dashboard

The project includes an interactive dashboard built around the machine learning pipeline.

### Dashboard Modules

#### 📈 Model Analytics

Provides visibility into model performance and analytical results.

#### 🔎 Dataset Explorer

Allows users to inspect and explore the underlying logistics data.

#### 📋 Project Information

Provides information about the platform, its purpose, architecture, and technology stack.

The dashboard is organized under:

```text
dashboard/
├── app.py
├── api.py
└── pages/
    ├── 1_Model_Analytics.py
    ├── 2_Dataset_Explorer.py
    └── 3_About_Projects.py
```

---

## ⚡ FastAPI Inference Layer

The project includes a dedicated API layer for model inference.

```text
ml/api/
├── __init__.py
├── app.py
├── predictor.py
└── schemas.py
```

### Responsibilities

* Load trained model artifacts
* Validate prediction inputs
* Transform incoming data
* Generate model predictions
* Return structured prediction responses

The API layer separates model inference from the dashboard and allows the ML system to be consumed as a service.

---

## 🧪 MLOps

The project incorporates MLOps principles to make the machine learning workflow more reproducible and maintainable.

### MLOps Components

* Experiment tracking
* Model artifacts
* Model comparison
* Reproducible training
* Serialized preprocessing pipelines
* Model versioning workflow
* Structured inference API

MLflow is used as part of the experiment tracking workflow.

---

## 🗂️ Data Pipeline

The project contains dedicated data directories:

```text
ml/data/
├── raw/
└── processed/
```

The repository also includes a data-generation component for creating logistics shipment data for experimentation and model development.

---

## 🛠️ Technology Stack

### Programming & Data

* Python
* Pandas
* NumPy

### Machine Learning

* Scikit-learn
* XGBoost
* LightGBM
* CatBoost

### Explainable AI

* SHAP
* Feature Importance Analysis

### API

* FastAPI

### Dashboard

* Streamlit

### MLOps

* MLflow

### Testing

* Python Testing Frameworks

### Development & Deployment

* Git
* GitHub
* Environment configuration
* Serialized ML artifacts

---

## 📂 Project Structure

```text
intelligent-logistics-platform/
│
├── dashboard/
│   ├── app.py
│   ├── api.py
│   └── pages/
│       ├── 1_Model_Analytics.py
│       ├── 2_Dataset_Explorer.py
│       └── 3_About_Projects.py
│
├── ml/
│   ├── api/
│   │   ├── app.py
│   │   ├── predictor.py
│   │   └── schemas.py
│   │
│   ├── data/
│   │   ├── raw/
│   │   └── processed/
│   │
│   ├── models/
│   │   ├── best_model.pkl
│   │   ├── random_forest.pkl
│   │   ├── random_forest_model.pkl
│   │   ├── delay_regression_model.pkl
│   │   ├── preprocessor.pkl
│   │   ├── feature_importance.csv
│   │   ├── model_comparison_results.csv
│   │   └── regression_results.csv
│   │
│   └── src/
│       ├── data_generation/
│       ├── explainability/
│       ├── models/
│       ├── feature_engineering.py
│       └── train.py
│
├── test_root_cause.py
├── requirements.txt
├── .env.example
├── .gitignore
├── LICENSE
└── README.md
```

---

## 💻 Installation

Clone the repository:

```bash
git clone https://github.com/ssrijan579-cell/intelligent-logistics-platform.git
```

Navigate to the project:

```bash
cd intelligent-logistics-platform
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Dashboard

Launch the Streamlit dashboard:

```bash
streamlit run dashboard/app.py
```

The dashboard provides access to model analytics, dataset exploration, and project information.

---

## ⚡ Running the API

The FastAPI inference service is located under:

```text
ml/api/
```

Run the API using:

```bash
uvicorn ml.api.app:app --reload
```

The API can then be accessed locally through the FastAPI server.

---

## 🧠 Training the Models

The main training workflow is located in:

```text
ml/src/train.py
```

Run:

```bash
python ml/src/train.py
```

The training pipeline generates model artifacts and evaluation results under:

```text
ml/models/
```

---

## 🧪 Running Tests

The repository includes automated testing for prediction/root-cause functionality.

Run:

```bash
pytest
```

---

## 📌 Model Artifacts

The repository maintains trained model and preprocessing artifacts including:

* Best-performing model
* Random Forest models
* Regression model
* Feature preprocessing pipeline
* Feature importance results
* Model comparison results
* Regression evaluation results

These artifacts allow the inference API to use previously trained models without retraining during every prediction request.

---

## 🔐 Environment Configuration

Environment configuration is provided through:

```text
.env.example
```

Create your local environment file:

```bash
cp .env.example .env
```

Add environment-specific values as required.

> Never commit API keys, credentials, passwords, or other secrets to GitHub.

---

## 📊 Business Applications

The platform can support logistics operations by helping teams:

* Identify high-risk shipments
* Prioritize operational interventions
* Understand major delay drivers
* Monitor shipment performance
* Compare model predictions
* Analyze logistics datasets
* Support proactive delivery management

---

## 🔮 Future Enhancements

Potential future improvements include:

* Real-time shipment tracking
* Automated model retraining
* Data drift detection
* Model monitoring
* Real-time alerts for high-risk shipments
* Advanced route-level analytics
* Automated operational recommendations
* LLM-powered logistics assistant
* Conversational analytics
* Cloud deployment
* CI/CD automation

---

## 🚧 Project Status

**Status: Completed ✅**

The core end-to-end logistics intelligence platform has been implemented, including:

* Machine learning pipeline
* Feature engineering
* Model training
* Model comparison
* Regression and classification workflows
* Model artifacts
* Explainability components
* FastAPI inference layer
* Streamlit analytics dashboard
* Dataset exploration
* Automated testing
* MLOps-oriented experiment tracking

The project can be further extended with production monitoring, real-time integrations, cloud infrastructure, and advanced AI capabilities.

---

## 👨‍💻 Author

**Srijan Srivastava**

🔗 GitHub: https://github.com/ssrijan579-cell

---

## ⭐ Project

If you find this project interesting, consider giving the repository a ⭐.

Built with **Python, Machine Learning, Explainable AI, FastAPI, Streamlit, and MLOps**.
