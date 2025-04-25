import pytest
from fastapi.testclient import TestClient


def test_api_home(client):
    """Test the home endpoint returns the welcome message."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"detail": "Welcome to FastAPI"}


def test_predict_endpoint(client, sample_client_data):
    """Test the /predict endpoint with valid client data."""
    # Prepare the request payload
    payload = {"inputs": sample_client_data}
    
    # Make the request
    response = client.post("/predict", json=payload)
    
    # Check response status and structure
    assert response.status_code == 200
    data = response.json()
    assert "predict_proba" in data
    assert "binary_prediction" in data
    
    # Check the content based on our mock model
    # Based on our mock model, it should return [0.3] for predict_proba
    # and [0] for binary_prediction for the first sample
    assert data["predict_proba"] == [0.3]  # Since we're only sending one client
    assert data["binary_prediction"] == [0]  # With threshold 0.5, this is 0


def test_predict_endpoint_invalid_data(client):
    """Test the /predict endpoint with invalid data."""
    # Missing required fields
    payload = {"inputs": [{"ORGANIZATION_TYPE": "Business Entity Type 3"}]}
    
    response = client.post("/predict", json=payload)
    assert response.status_code == 422  # Validation error


def test_predict_by_id_endpoint_found(client):
    """Test the /predict_by_id endpoint with an ID that exists."""
    # Use an ID that exists in our mock test set
    payload = {"client_id": 100001}
    
    response = client.post("/predict_by_id", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert "predict_proba" in data
    assert "binary_prediction" in data


def test_predict_by_id_endpoint_not_found(client, monkeypatch):
    """Test the /predict_by_id endpoint with an ID that doesn't exist."""
    # Create an error message for debugging
    
    # Use an ID that doesn't exist
    payload = {"client_id": 999999}
    
    response = client.post("/predict_by_id", json=payload)
    assert response.status_code == 404
    assert response.json() == {"detail": "Client ID not found"}