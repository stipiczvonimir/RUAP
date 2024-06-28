import streamlit as st
import urllib.request
import json
import ssl
import os

# Function to allow self-signed HTTPS connections
def allow_self_signed_https(allowed):
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

# Set this to True if using a self-signed certificate
allow_self_signed_https(False)

# Azure ML endpoint URL and API key
endpoint = "http://cd98a830-a1da-421b-80d0-e5d1a4994489.northeurope.azurecontainer.io/score"
api_key = "M0jF9xHZpi4VqvSymjlth7Q0dAkSFHZm"

st.title("💼 Salary Prediction App")

# Collect inputs
experience_level = st.selectbox("Experience Level", ["EN", "MI", "SE", "EX"])
job_title = st.text_input("Job Title")
company_location = st.selectbox("Company Location", ["US"])
company_size = st.selectbox("Company Size", ["S", "M", "L"])

# Function to make the prediction request
def get_prediction(data):
    try:
        # Prepare the data payload in JSON format
        payload = {
            "Inputs": {
                "data": [
                    {
                        "experience_level": data["experience_level"],
                        "job_title": data["job_title"],
                        "company_location": data["company_location"],
                        "company_size": data["company_size"]
                    }
                ]
            },
            "GlobalParameters": 1.0
        }

        # Encode the payload as JSON
        body = json.dumps(payload).encode('utf-8')

        # Prepare headers with API key
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }

        # Make the HTTP POST request to the Azure ML endpoint
        req = urllib.request.Request(endpoint, body, headers)
        response = urllib.request.urlopen(req)

        # Read and return the prediction result
        result = response.read().decode('utf-8')
        return json.loads(result)

    except Exception as e:
        st.error(f"Prediction error: {e}")




if st.button("Predict"):
    input_data = {
        "experience_level": experience_level,
        "job_title": job_title,
        "company_location": company_location,
        "company_size": company_size
    }

    prediction_result = get_prediction(input_data)
    
    if prediction_result and "Results" in prediction_result:
        predicted_salary = prediction_result["Results"][0]
        st.markdown("## 📊 Prediction Result")
        st.success(f"The predicted salary is: ${predicted_salary:,.2f}")
    else:
        st.error("Failed to get a prediction. Please check your input and try again.")
