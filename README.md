---
title: API_mlmodel
emoji: 🫥
colorFrom: indigo
colorTo: gray
sdk: docker
app_file: app.py
pinned: false
---

# oc_p7_APItothecloud API

This Space hosts a FastAPI application that predicts credit risk for loan applicants.

## API Documentation

Once deployed, you can access the API documentation at:
- `/docs` - Swagger UI documentation
- `/redoc` - ReDoc documentation

## Endpoints

- `GET /` - Welcome message and basic information
- `POST /predict` - Make predictions with client data
- `POST /predict_by_id` - Make predictions using client ID from test set

## Example Usage

```python
import requests
import json

# API endpoint URL
url = "https://huggingface.co/spaces/Calhenry/API_mlmodel/predict"

# Sample client data
client_data = {
    "inputs": [
        {
            "ORGANIZATION_TYPE": "Business Entity Type 3",
            "DAYS_EMPLOYED": 3650,
            "OCCUPATION_TYPE": "Core staff",
            "NAME_FAMILY_STATUS": "Married",
            "NAME_EDUCATION_TYPE": "Higher education",
            "CODE_GENDER": "M",
            "WEEKDAY_APPR_PROCESS_START": "MONDAY",
            "FLAG_OWN_CAR": "Y",
            "NAME_CONTRACT_TYPE": "Cash loans",
            "NAME_INCOME_TYPE": "Working",
            "NAME_HOUSING_TYPE": "House / apartment",
            "REGION_RATING_CLIENT": 1,
            "WALLSMATERIAL_MODE": "Stone, brick",
            "NAME_TYPE_SUITE": "Spouse, partner",
            "FLAG_OWN_REALTY": "Y"
        }
    ]
}

# Make the API call
response = requests.post(url, json=client_data)

# Display the result
print(response.status_code)
print(response.json())
```

## About the Model

This API uses a LightGBM model trained to predict credit risk. The model was trained on the 15 most important features identified during model development.
