"""
Configuration file for pytest to handle common fixtures
and setup for testing the Credit Risk Prediction FastAPI app.
"""

import os
import sys
from unittest import mock

import pytest
import joblib
import numpy as np
import pandas as pd
from fastapi.testclient import TestClient

# Add the parent directory to sys.path to allow importing app.py
# This ensures imports work properly for both direct pytest runs and GitHub Actions
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))

# Mock the joblib.load function to return the mock objects
@pytest.fixture
def mock_joblib_load(monkeypatch, mock_model_info, mock_preprocessor, mock_test_set):
    def mock_load(filename):
        if "lgbm_model" in filename:
            return mock_model_info
        elif "preprocessor" in filename:
            return mock_preprocessor
        elif "app_test_domain" in filename:
            return mock_test_set
        else:
            raise FileNotFoundError(f"Mock couldn't find {filename}")

    # Apply the mock to joblib.load
    monkeypatch.setattr(joblib, "load", mock_load)

@pytest.fixture
def mock_model_info():
    # Create a mock model_info dictionary
    class MockModel:
        def predict_proba(self, X):
            # Return mock probabilities for 2 samples
            return np.array([[0.7, 0.3], [0.2, 0.8]])

    return {"name": "LGBM Model", "best_model": MockModel(), "best_threshold": 0.5}


@pytest.fixture
def mock_preprocessor():
    # Create a mock preprocessor that returns transformed data
    class MockPreprocessor:
        def transform(self, X):
            # Simply return a numpy array of the same length as input
            return np.ones((len(X), 10))

    return MockPreprocessor()


@pytest.fixture
def mock_test_set():
    # Create a small mock test dataset with client IDs
    data = {
        "SK_ID_CURR": [100001, 100002],
        "ORGANIZATION_TYPE": ["Business Entity Type 3", "School"],
        "DAYS_EMPLOYED": [-1000, -2000],
        "OCCUPATION_TYPE": ["Laborers", "Managers"],
        "NAME_FAMILY_STATUS": ["Single / not married", "MarriedCivil marriage"],
        "NAME_EDUCATION_TYPE": ["Secondary / secondary special", "Higher education"],
        "CODE_GENDER": ["M", "F"],
        "WEEKDAY_APPR_PROCESS_START": ["MONDAY", "TUESDAY"],
        "FLAG_OWN_CAR": ["Y", "N"],
        "NAME_CONTRACT_TYPE": ["Cash loans", "Revolving loans"],
        "NAME_INCOME_TYPE": ["Working", "State servant"],
        "NAME_HOUSING_TYPE": ["House / apartment", "Rented apartment"],
        "REGION_RATING_CLIENT": [1, 2],
        "WALLSMATERIAL_MODE": ["Stone, brick", "Panel"],
        "NAME_TYPE_SUITE": ["Unaccompanied", "Family"],
        "FLAG_OWN_REALTY": ["Y", "N"],
    }
    return pd.DataFrame(data)


@pytest.fixture
def sample_client_data():
    # Sample data for multiple clients in the format expected by the API
    return [
        {
            "ORGANIZATION_TYPE": "Business Entity Type 3",
            "DAYS_EMPLOYED": -1000,
            "OCCUPATION_TYPE": "Laborers",
            "NAME_FAMILY_STATUS": "Single / not married",
            "NAME_EDUCATION_TYPE": "Secondary / secondary special",
            "CODE_GENDER": "M",
            "WEEKDAY_APPR_PROCESS_START": "MONDAY",
            "FLAG_OWN_CAR": "Y",
            "NAME_CONTRACT_TYPE": "Cash loans",
            "NAME_INCOME_TYPE": "Working",
            "NAME_HOUSING_TYPE": "House / apartment",
            "REGION_RATING_CLIENT": 1,
            "WALLSMATERIAL_MODE": "Stone, brick",
            "NAME_TYPE_SUITE": "Unaccompanied",
            "FLAG_OWN_REALTY": "Y",
        }
    ]


@pytest.fixture
def client(mock_joblib_load):
    # This fixture creates a TestClient
    from app import app
    return TestClient(app)