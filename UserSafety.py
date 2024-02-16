# 1. USER SAFETY: It will be checking if you have accessed any malicious site over the past 24 hour, by scanning through your web browser information locally. This process is taking place locally and once list is created it passes to another class. We use two things first our list of inbuilt dataset of safe and unsafe sites, next is scanning the unidentified sites and flagging them.  Now for the scanning part we will be checking multiple factors and will be using somewhat binary classification of ML, i.e. we will be checking if the site follows a "quick change algorithm" for dynamic changing sites, suspicious regex, and other things similar to it.

import os
import sqlite3
import random
from datetime import datetime, timedelta

# Adding safe and unsafe sites
safeSites = []
unsafeSites = []

# Dynamic changing sites and suspicious regex
quickChangeAlgorithm = [0.5 , 0.7]

def evaluate_site(url):
    if ".orion" in url:
        unsafeSites.append(url)
        print(f"Unsafe site: {url}")
    else:
        # Add additional logic to evaluate the site and determine if it is safe or unsafe
        # You can use quickChangeAlgorithm or suspiciousRegex lists for more evaluation criteria
        # For now, let's assume it's unsafe if not in safeSites

        reward = simulate_reward(url)

        if quickChangeAlgorithm and len(quickChangeAlgorithm) >= 2:
            if reward > quickChangeAlgorithm[0]:
                safeSites.append(url)
                print(f"Safe site: {url}")
            elif reward < quickChangeAlgorithm[1]:
                unsafeSites.append(url)
                print(f"Unsafe site: {url}")
            else:
                # Continue monitoring or take default action
                print(f"Continue monitoring: {url}")
        else:
            # Handle the case where quickChangeAlgorithm is not properly defined
            print("Quickest Change Algorithm not properly defined")

def simulate_reward(url):
    # Replace this 

    keyword_weightage = {
        "important": 0.9,
        "security": 0.85,
        "entertainment": 0.7,
        "shopping": 0.8,
        "education": 0.75
    }

    for keyword, weightage in keyword_weightage.items():
        if keyword in url:
            # If the keyword is present in the URL, return the associated weightage as reward
            return random.uniform(weightage, 1.0)
    
    # If none of the keywords are present, return a default low to medium reward
    return random.uniform(0.0, 0.7)

# Code to scan through the web browser information
data_path = os.path.join("/home/arpitgupta/.mozilla/firefox/2ozbvcyu.default-release/")
history_db = os.path.join(data_path, 'places.sqlite')

c = sqlite3.connect(history_db)

cursor = c.cursor()

# Calculate the timestamp for 24 hours ago
twenty_four_hours_ago = datetime.utcnow() - timedelta(hours=1)
timestamp_24_hours_ago = int(twenty_four_hours_ago.timestamp() * 1e6)

select_statement = "SELECT url, visit_count FROM moz_places WHERE last_visit_date >= ?;"
cursor.execute(select_statement, (timestamp_24_hours_ago,))


results = cursor.fetchall()

# Check if the site is safe or unsafe
for url, count in results:
    if url in safeSites:
        continue
    elif url in unsafeSites:
        print(f"Unsafe site: {url}")
    else:
        evaluate_site(url)

# Close the cursor and connection
cursor.close()
c.close()


# # code to delete the list and history accessed
# safeSites.clear()
# unsafeSites.clear()
# os.remove(history_db)
# # End of snippet