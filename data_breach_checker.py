import requests
from dotenv import load_dotenv
import os
from colorama import Fore, Style
import sys

# Load variables from the .env file


email = input("Your email ? ")
print()
print("The data can be sorted in the following categories")
print()
print(f"{Style.BRIGHT}{Fore.YELLOW}1) {Fore.RESET}Sort by domain{Style.RESET_ALL}")
print(f"{Style.BRIGHT}{Fore.YELLOW}2) {Fore.RESET}Sort by date")

print("\nChoose a category (number): ", end="")
category = int(input())
print()


load_dotenv()

api_key = os.getenv("API_KEY_DATA_BREACH")

url = "https://data-breach-checker.p.rapidapi.com/api/breach"

querystring = {"email": email}

headers = {
    "X-RapidAPI-Key": api_key,
    "X-RapidAPI-Host": "data-breach-checker.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)
data = response.json().get('data', [])  # Get data or empty list if 'data' is not in response

if not data:  # If data is empty
    print(f"{Style.BRIGHT}{Fore.GREEN}You have not been breached!{Style.RESET_ALL}")
    sys.exit()

# Initialize dictionaries to categorize breaches
domain_categories = {}
breach_date_categories = {}

# Categorize breaches
for breach in data:
    domain = breach['Domain']
    if domain not in domain_categories:
        domain_categories[domain] = []
    domain_categories[domain].append(breach)

    breach_date = breach['BreachDate']
    if breach_date not in breach_date_categories:
        breach_date_categories[breach_date] = []
    breach_date_categories[breach_date].append(breach)

if category == 1:

    # Display breaches by domain
    print(f"{Style.BRIGHT}{Fore.YELLOW}Breaches categorized by Domain:{Fore.RESET}{Style.RESET_ALL}")
    for domain, breaches in domain_categories.items():
        print(f"\nBreaches related to {domain}:")
        for breach in breaches:
            print(f"\n{Style.BRIGHT}{Fore.BLUE}Name: {breach['Name']}{Fore.RESET}{Style.RESET_ALL}")
            print(f"{Style.BRIGHT}{Fore.BLUE}Description{Fore.RESET}{Style.RESET_ALL}: {breach['Description']}")
            print(f"{Style.BRIGHT}{Fore.BLUE}Breach Date{Fore.RESET}:{Style.RESET_ALL}{breach['BreachDate']}")
            print("------------------------------------------")

elif category == 2:

    # Display breaches by breach date
    print(f"{Style.BRIGHT}{Fore.YELLOW}Breaches categorized by Breach Date:{Fore.RESET}{Style.RESET_ALL}")
    for breach_date, breaches in breach_date_categories.items():
        print(f"\nBreaches occurred on {breach_date}:")
        for breach in breaches:
            print(f"\n{Style.BRIGHT}{Fore.BLUE}Name: {breach['Name']}{Fore.RESET}{Style.RESET_ALL}")
            print(f"{Style.BRIGHT}{Fore.BLUE}Description{Fore.RESET}{Style.RESET_ALL}: {breach['Description']}")
            print(f"{Style.BRIGHT}{Fore.BLUE}Domain{Fore.RESET}{Style.RESET_ALL}: {breach['Domain']}")
            print("------------------------------------------")
else:
    print(f"{Style.BRIGHT}{Fore.RED}Invalid Category! Please enter either 1 or 2.{Fore.RESET}{Style.RESET_ALL}")
    sys.exit()
