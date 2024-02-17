from colorama import Fore, Style
import sys
import subprocess
import os


logo = """
 _   _            _   ______      _ _      ______       _    
| | | |          | |  | ___ \    | | |     | ___ \     | |   
| |_| | __ _  ___| | _| |_/ / ___| | |___  | |_/ / ___ | |_  
|  _  |/ _` |/ __| |/ / ___ \/ _ \ | / __| | ___ \/ _ \| __| 
| | | | (_| | (__|   <| |_/ /  __/ | \__ \ | |_/ / (_) | |_  
\_| |_/\__,_|\___|_|\_\____/ \___|_|_|___/ \____/ \___/ \__| 
                                                             
"""

print(logo)


# Logic starts

print(f'{Style.BRIGHT}The following tools are available: {Style.RESET_ALL}')
print()

print(f"{Style.BRIGHT}{Fore.YELLOW}1) {Fore.RESET}Your browser history safety{Style.RESET_ALL}")
print(f"{Style.BRIGHT}{Fore.YELLOW}2) {Fore.RESET}Is your email exposed ? {Style.RESET_ALL}")
print(f"{Style.BRIGHT}{Fore.YELLOW}3) {Fore.RESET}Check Phishing link.{Style.RESET_ALL}")
print(f"{Style.BRIGHT}{Fore.YELLOW}4) {Fore.RESET}Perform Deep Crawling [For Professionals]{Style.RESET_ALL}")

print()


print(f"{Style.BRIGHT}{Fore.BLACK} Tool you want to use? {Fore.RESET} {Style.RESET_ALL}")

user_choice = int(input())

if  user_choice == 1 :
    subprocess.run(["python3", 'UserSafety.py'])
elif user_choice == 2 :
    subprocess.run(["python3", "data_breach_checker.py"])
elif user_choice == 3 :
    subprocess.run(["python3", "PhishingCheck.py"])
elif user_choice == 4 :
    directory = 'DaCrBot'
    os.chdir(directory)
    subprocess.run("scrapy crawl site_crawler -O data.csv", shell=True)
else :
    print("Exiting the program...")
    sys.exit()