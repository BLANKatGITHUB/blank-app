import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import ipaddress
from urllib.parse import urlparse, parse_qs
from url_preprocessing import shannon_entropy, is_ip_address,preprocessing
import streamlit as st

def extract_features(url):
    features = {}
    
    # Basic URL features
    features["url_length"] = len(url)
    features["dot_count"] = url.count(".")
    features["slash_count"] = url.count("/")
    features["dash_count"] = url.count("-")
    features["underscore_count"] = url.count("_")
    features["at_count"] = url.count("@")
    features["question_count"] = url.count("?")
    features["equal_count"] = url.count("=")
    features["and_count"] = url.count("&")
    features["digit_count"] = sum(c.isdigit() for c in url)
    features["letter_count"] = sum(c.isalpha() for c in url)
    
    # Protocol and existence of common patterns
    features["starts_with_http"] = int(url.startswith("http://"))
    features["starts_with_https"] = int(url.startswith("https://"))
    features["has_www"] = int("www" in url)
    
    # Parse URL for detailed components
    parsed = urlparse(url)
    host = parsed.netloc.lower()  # domain part
    path = parsed.path
    query = parsed.query
    
    # Domain and subdomain features
    host_parts = host.split('.')
    # Assume the last two parts form the registered domain (this is a simplification)
    if len(host_parts) >= 2:
        registered_domain = ".".join(host_parts[-2:])
        subdomains = host_parts[:-2]
    else:
        registered_domain = host
        subdomains = []

    features["subdomain_count"] = len(subdomains)
    features["registered_domain_length"] = len(registered_domain)
    
    # Check if the host is an IP address
    features["is_ip_address"] = is_ip_address(host)
    
    # Top-Level Domain (TLD) features
    # Assume TLD is last part after the final '.'
    if '.' in registered_domain:
        tld = registered_domain.split('.')[-1]
    else:
        tld = ''
    features["tld_length"] = len(tld)
    
    # Ratio of digits to letters in URL (avoid division by zero)
    features["digit_letter_ratio"] = (features["digit_count"] / features["letter_count"]) if features["letter_count"] else 0
    
    # Entropy of the domain
    features["domain_entropy"] = shannon_entropy(host)
    
    # Path depth: count of subdirectories (ignoring the initial slash)
    # Remove trailing slash if present.
    cleaned_path = path.rstrip('/')
    features["path_depth"] = len(cleaned_path.split('/')) - 1 if cleaned_path else 0
    
    # Query features: number of parameters in the query string
    query_dict = parse_qs(query)
    features["query_param_count"] = len(query_dict)
    
    return features

# function to extract features from dataset
# This function assumes the dataset is in CSV format and has a column named 'url'
# and that the dataset is located in the same directory as this script.
def extract_features_from_dataset(dataset_path):
    df = pd.read_csv(dataset_path)
    df_features = df['url'].apply(extract_features)
    features_df = pd.DataFrame(df_features.tolist())
    features_df['status'] = df['status'] 
    return features_df


# function to generate graphs for the selected features
# This function takes the dataset features and user features as input
def generate_graphs(dataset_features, user_features):
    selected_features = [
        "url_length",
        "digit_count",
        "path_depth",
        "query_param_count",
        "domain_entropy",
    ]
    
    for feature in selected_features:
        plt.figure(figsize=(10, 6))
        sns.histplot(
            data=dataset_features, 
            x=feature, 
            hue="status", 
            kde=True, 
            bins=30, 
            palette={"phishing": "red", "legitimate": "green"}, 
            alpha=0.7
        )
        plt.axvline(
            user_features[selected_features.index(feature)], 
            color='orange', 
            linestyle='--', 
            linewidth=2, 
            label="User URL"
        )
        plt.title(f"Feature: {feature}", fontsize=16, fontweight='bold', color='darkblue')
        plt.legend(
            title="Legend",
            labels=["Phishing (red)", "Legitimate (green)", "User URL (orange)"],
            fontsize=12
        )
        plt.xlabel(feature, fontsize=14, fontweight='bold')
        plt.ylabel("Frequency", fontsize=14, fontweight='bold')
        plt.grid(axis='y', linestyle='--', alpha=0.6)
        sns.despine()
        st.pyplot(plt)
        plt.clf()
