import streamlit as st
from url_preprocessing import preprocessing
import pickle
from url_graphs import extract_features_from_dataset, generate_graphs
import urllib.parse

st.title("Phishing URL Detector")
st.write(
    "This is a simple web application that uses a machine learning model to detect phishing URLs. Please enter a URL below to check if it is phishing or not."
)

with st.sidebar:
    st.header("About")
    st.write("This app detects phishing URLs using a machine learning model.")
    st.write("Dataset: `dataset_phishing.csv`")
    st.write("Model: `rf_model.pkl`")

url = st.text_input("Enter a URL:")

def load_model(filepath):
    with open(filepath, "rb") as f:
        return pickle.load(f)

def validate_url(url):
    parsed_url = urllib.parse.urlparse(url)
    return parsed_url.scheme and parsed_url.netloc

# Main logic
if url:
    if not validate_url(url):
        st.error("Please enter a valid URL.")
    else:
        with st.spinner("Processing..."):
            try:
                # Load the model
                model = load_model("rf_model.pkl")

                # Preprocess the URL
                features = preprocessing(url)
                features = [features]  # Reshape for prediction

                # Make a prediction
                prediction = model.predict(features)

                if prediction[0] == 0:
                    st.success("This URL is likely to be phishing.")
                else:
                    st.success("This URL is likely to be safe.")

                # After prediction
                confidence = model.predict_proba(features)[0]  
                st.metric(label="Prediction Confidence", value=f"{confidence[1]*100:.2f}%" if prediction[0] == 1 else f"{confidence[0]*100:.2f}%")

                # Generate graphs
                dataset_features = extract_features_from_dataset("dataset_phishing.csv") 
                
                # Placeholder for graphs
                st.subheader("Feature Analysis")
                generate_graphs(dataset_features, features[0])
            except Exception as e:
                st.error(f"An error occurred: {e}")
