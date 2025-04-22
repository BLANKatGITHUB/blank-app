import streamlit as st
from url_preprocessing import preprocessing
import pickle
from url_graphs import extract_features_from_dataset, generate_graphs

st.title("Phishing URL Detector")
st.write(
    "This is a simple web application that uses a machine learning model to detect phishing URLs. Please enter a URL below to check if it is phishing or not."
)

url = st.text_input("Enter a URL:")

if url:
    # Load the model
    with open("rf_model.pkl", "rb") as f:
        model = pickle.load(f)

    # Preprocess the URL
    features = preprocessing(url)
    features = [features]  # Reshape for prediction

    # Make a prediction
    prediction = model.predict(features)

    if prediction[0] == 0:
        st.write("This URL is likely to be phishing.")
    else:
        st.write("This URL is likely to be safe.")

    dataset_features = extract_features_from_dataset("dataset_phishing.csv") 
    generate_graphs(dataset_features, features[0])
