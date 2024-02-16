from urllib.parse import urlparse
import ssl
import socket
from bs4 import BeautifulSoup
import requests

safe_urls = []
unsafe_urls = []

# Section 1: HTML Analysis
def html_analysis_score(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Add your own criteria to check for suspicious content within the HTML.
        suspicious_content = soup.find_all("script", {"src": "malicious-script.js"})
        return len(suspicious_content)
    except Exception as e:
        print(f"Error in HTML analysis: {e}")
        return 0

# Section 2: SSL Certificate Check
def ssl_certificate_score(url):
    try:
        parsed_url = urlparse(url)
        context = ssl.create_default_context()
        with context.wrap_socket(socket.socket(), server_hostname=parsed_url.netloc) as s:
            s.connect((parsed_url.netloc, 443))
        return 0  # No SSL issues
    except ssl.SSLCertVerificationError:
        return 1  # SSL certificate issue

# Section 3: PhishStats API Check
def check_phishstats_info(url):
    phishstats_api_url = "https://phishstats.info:2096/api/phishing"
    params = {"_p": 1, "_size": 50}  # Adjust parameters as needed

    try:
        response = requests.get(phishstats_api_url, params=params)
        if response.status_code == 200:
            data = response.json()
            for entry in data:
                if entry["url"].lower() == url.lower():
                    print(f"The URL '{url}' is listed in PhishStats with details:")
                    print(f"IP: {entry['ip']}, Country: {entry['countryname']}, City: {entry['city']}")
                    return 3  # Phishing site according to PhishStats
            print(f"The URL '{url}' is not found in PhishStats.")
            return 0
        else:
            print(f"Failed to fetch data from PhishStats. Status code: {response.status_code}")
            return 0
    except Exception as e:
        print(f"Error checking PhishStats: {e}")
        return 0

# Section 4: Another HTML Analysis
def additional_html_analysis_score(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Add additional criteria for HTML analysis.
        return 0  # Placeholder for additional analysis points
    except Exception as e:
        print(f"Error in additional HTML analysis: {e}")
        return 0

# Placeholder for local safe/unsafe check
def check_in_local_safe_unsafe(url):
    # Implement logic to check against local safe/unsafe list
    return False  # Replace with your logic

# User input for the URL
user_url = input("Enter the URL to check for phishing: ")

# Check in local safe/unsafe list
if check_in_local_safe_unsafe(user_url):
    print(f"The URL '{user_url}' is in the local safe list.")
    # Optionally, you can add code to exit or return here.
else:
    # Calculate scores for each section
    html_analysis_points = html_analysis_score(user_url)
    ssl_certificate_points = ssl_certificate_score(user_url)
    phishstats_info_points = check_phishstats_info(user_url)
    additional_html_analysis_points = additional_html_analysis_score(user_url)

    # Calculate total points
    total_points = html_analysis_points + ssl_certificate_points + phishstats_info_points + additional_html_analysis_points

    # Set a threshold for potential phishing
    threshold = 5

    # Check if total points exceed the threshold
    if total_points >= threshold:
        print(f"The URL '{user_url}' might be a phishing site. Total points: {total_points}")
        unsafe_urls.append(user_url)  # Add to the unsafe list
        # Optionally, you can add code to send a notification or take further action.
    else:
        print(f"The URL '{user_url}' is less likely to be a phishing site. Total points: {total_points}")
        safe_urls.append(user_url)  # Add to the safe list

# Implement further actions or reporting as needed.
