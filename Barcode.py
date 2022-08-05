####################################################################################################

from getpass import getpass
import os
import json
import time
import tkinter as tk
import requests
from requests.structures import CaseInsensitiveDict

####################################################################################################

notScanned = True
programActive = True
HEIGHT = 400
WIDTH = 400


try:
    authKey = open("authKey.txt", "r").read()
    krogerToken = json.loads((open("privateKrogerTokens.json","r")).read())["access_token"]
    krogerRefreshToken = json.loads((open("privateKrogerTokens.json","r")).read())["refresh_token"]

except:
    newAccount = True
    print("Error: No authKey and/or Token info found. Manually add these files with relevant data")
    while True:
        time.sleep(1)

####################################################################################################

def refreshKrogerTokens():
    global krogerToken
    global krogerRefreshToken

    #sends refresh token api request
    url = "https://api.kroger.com/v1/connect/oauth2/token"
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    headers["Authorization"] = f"Basic {authKey}"
    data = f"grant_type=refresh_token&refresh_token={krogerRefreshToken}"

    #reads response to json
    resp = requests.post(url, headers=headers, data=data)
    file = open("returnedKrogerTokens.json", "w")
    file.write(json.dumps(resp.json(), indent = 2))
    file = open("returnedKrogerTokens.json","r")
    tokenArray = json.loads(file.read())

    #resets krogerTokens and privateKrogerTokens file while checking for error
    try:
        krogerToken = tokenArray["access_token"]
        krogerRefreshToken = tokenArray["refresh_token"]
        file = open("privateKrogerTokens.json", "w")
        file.write(json.dumps(resp.json(),indent = 2))
        file = open("privateKrogerTokens.json","r")
        tokenArray = json.loads(file.read())

    except:
        "Token Error: Manually Refresh KrogerTokens"
    
    return time.time()

def addItemToCart(id):
    global krogerToken
    os.system("rm -f cart.json")

    #sends cart add api request
    url = "https://api.kroger.com/v1/cart/add"
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {krogerToken}"
    headers["Content-Type"] = "application/x-www-form-urlencoded"

    data = """
    {
      "items": [
        {
        "upc": """+f"\"{id}\""+""",
        "quantity": 1
        }
        ]
    }
    """

    #writes response to a file
    resp = requests.put(url, headers=headers, data=data)
    c = open("cart.json", "w")
    try: resp.json()
    except: print("Sent Successfully")
    else: c.write(json.dumps(resp.json(),indent = 2))

def addToInventory(id, description):

    file = open("inventory.json", "r")
    fileString = file.read()
    inventoryArray = json.loads(fileString)

    try:
        inventoryArray["item_upcs"][0][id][0]["quantity"]+=1
        file = open("inventory.json", "w")
        file.write(json.dumps(inventoryArray))
    except:
        newItemArray = f"{{\"{id}\":[{{\"item\":\"{description}\",\"quantity\":1}}]}},"
        fileString = fileString[:15]+newItemArray+fileString[15:]
        file = open("inventory.json", "w")
        file.write(fileString)

def getInfoOfScannedItem(id):
    global krogerToken
    os.system("rm -f productInfo.json")

    #commented code displays the upc value that will be sent for debugging purposes with scanner
    # os.system("clear")
    # print(id)
    # time.sleep(2)

    #sends item info api request
    url = f"https://api.kroger.com/v1/products?filter.productId={id}"
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {krogerToken}"

    #writes response to json while checking for the different error types
    resp = requests.get(url, headers=headers)
    file = open("productInfo.json", "w")
    file.write(json.dumps(resp.json(),indent = 2))
    file = open("productInfo.json", "r")
    infoList = json.loads(file.read())
    try: 
        print("Scanned item:",infoList["data"][0]["description"])
        try: 
            addToInventory(id, infoList["data"][0]["description"])
        except:
            print("Couldn't add to inventory")
    except: 
        
        try:
            print("Error: ", infoList["errors"]["reason"])

        except: 
            try:
                burner = infoList["pagination"]["warnings"][0]
                print("Error: Product ID wasn't found")
            except:
                print("Likely couldn't access due to krogerTokens: try manually resetting them")

        return False
    return True
####################################################################################################

while programActive:

    #reset krogerTokens 
    print("Refreshing krogerTokens for Updated Authentication...")
    timeOfLastRefresh = refreshKrogerTokens()
    print("Done!")

    while time.time()<timeOfLastRefresh+60 and programActive:
        #asks to scan item, then finds the info of that item and adds to cart
        id = ("00" + getpass("Scan an Item:"))[:13]
        if id[:12] == "000000000000":
            programActive = False
        os.system("clear")
        if getInfoOfScannedItem(id):
            addItemToCart(id)

        # Below code lets you end program by typing just 0 (then entering)
        # if input("Enter 0 to exit program, or anything else to continue") == "0":
        #     programActive = False
####################################################################################################