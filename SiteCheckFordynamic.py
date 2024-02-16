import requests
from bs4 import BeautifulSoup
import hashlib
import time
import os

def get_page_content(url):
    response = requests.get(url)
    return response.text

def hash_content(content):
    sha256 = hashlib.sha256()
    sha256.update(content.encode('utf-8'))
    return sha256.hexdigest()

def save_reference_hash(hash_value, instance_id):
    filename = f"reference_hash_{instance_id}.txt"
    with open(filename, "w") as file:
        file.write(hash_value)

def load_reference_hash(instance_id):
    filename = f"reference_hash_{instance_id}.txt"
    try:
        with open(filename, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

def main(instance_id):
    url = "https://youtube.com"  # Replace with the URL of the website you want to monitor
    reference_hash = load_reference_hash(instance_id)

    if reference_hash is None:
        print(f"No reference hash found for instance {instance_id}. Saving initial reference hash.")
        content = get_page_content(url)
        reference_hash = hash_content(content)
        save_reference_hash(reference_hash, instance_id)

    while True:
        content = get_page_content(url)
        current_hash = hash_content(content)

        if current_hash != reference_hash:
            print(f"Content has changed since reference time (t=0) for instance {instance_id}!")
            # You can add further actions or notifications here

        time.sleep(60)  # Wait for 60 seconds before checking again

if __name__ == "__main__":

    instance_id = os.environ.get('INSTANCE_ID', 'default')
    main(instance_id)
