import requests
from dotenv import load_dotenv
import os

# Load variables from the .env file
load_dotenv()

api_key = os.getenv("API_KEY_DATA_BREACH")

url = "https://data-breach-checker.p.rapidapi.com/api/breach"

querystring = {"email":"arpitb.lgupta1@gmail.com"}

headers = {
	"X-RapidAPI-Key": api_key,
	"X-RapidAPI-Host": "data-breach-checker.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())