import os
import requests
import datetime
import names
import time
import random
from bs4 import BeautifulSoup as bs
import json
import urllib3
import random

from colorama import Fore, Style, init
from faker import Faker

session = requests.Session()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
fake = Faker()
fake.locale = "en-US"

def create():
    global session

    csrfTokenURL = "https://www.footlocker.com/api/v3/session?timestamp=1582450101670"
    createAccountURL = "https://www.footlocker.com/api/v3/users?timestamp=1582454868099"
    data = userInfo()

    createAccHeaders = {
        'Host': 'www.footlocker.com',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Mobile Safari/537.36',
        'origin': 'https://www.footlocker.com',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Connection': 'keep-alive'
    }

    payload = {
        "bannerEmailOptIn": False,
        "preferredLanguage": "en",
        "firstName": data["fName"],
        "lastName": data["lName"],
        "postalCode": data["zipCode"],
        "uid": data["email"],
        "phoneNumber": data["phone"],
        "birthday": data["birthday"],
        "password": data["password"],
        "loyaltyStatus": True,
        "wantToBeVip": False,
        "referralCode": data["refCode"],
        "flxTcVersion": "2.0",
        "loyaltyFlxEmailOptIn": False
    }

    # Get cookies
    print(time.strftime("[%H:%M:%S]") + Fore.CYAN + 'Grabbing cookies from home page')
    session.get('https://www.footlocker.com',headers=createAccHeaders,verify=False)
    time.sleep(1)

    # Get the csrf token
    print(time.strftime("[%H:%M:%S]") + Fore.YELLOW + 'Getting session token')

    tokenReq = session.get(url=csrfTokenURL,headers=createAccHeaders,verify=False)
    tokenJSON = tokenReq.json()
    token = tokenJSON["data"]["csrfToken"]

    print(time.strftime("[%H:%M:%S]") + Fore.LIGHTYELLOW_EX + 'Got token: ' + token)
    time.sleep(1)

    # Create the account
    session.headers.update({'x-csrf-token':token})
    createReq = session.post(url=createAccountURL,headers=createAccHeaders,verify=False,json=payload)

    if (createReq.status_code == 201):
        print(time.strftime("[%H:%M:%S]") + Fore.LIGHTGREEN_EX + "Account created! " + data["email"])
    else:
        print(time.strftime("[%H:%M:%S]") + Fore.LIGHTRED_EX + "ERROR: " + createReq.text)

def userInfo():
    ref = input("Enter a ref code: ")
    user = {
        "email": fake.email().split("@")[0]+"@sjbb.world",
        "fName": fake.name().split(" ")[0],
        "lName": fake.name().split(" ")[1],
        "zipCode": "9"+genRandomXNumbers(4),
        "birthday": fake.month()+"/"+fake.day_of_month()+"/"+fake.year(),
        "password": fake.name().split(" ")[0]+"1S!",
        "phone": "909"+genRandomXNumbers(7),
        "refCode": ref 
    }

    return user
    
def genRandomXNumbers(n):
    num = ""
    for i in range(0 , n):
        num += str(random.randint(0,9))
    return num

create()