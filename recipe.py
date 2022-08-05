####################################################################################################################
####################################################################################################################
#####                                                                                                          #####
#####            ooooo     ooo ooooo      ooo ooooo     ooo  .oooooo..o oooooooooooo oooooooooo.               #####
#####            `888'     `8' `888b.     `8' `888'     `8' d8P'    `Y8 `888'     `8 `888'   `Y8b              #####
#####             888       8   8 `88b.    8   888       8  Y88bo.       888          888      888             #####
#####             888       8   8   `88b.  8   888       8   `"Y8888o.   888oooo8     888      888             #####
#####             888       8   8     `88b.8   888       8       `"Y88b  888    "     888      888             #####
#####             `88.    .8'   8       `888   `88.    .8'  oo     .d8P  888       o  888     d88'             #####
#####               `YbodP'    o8o        `8     `YbodP'    8""88888P'  o888ooooood8 o888bood8P'               #####
#####                                                                                                          #####
#####    ooooooooo.   ooooooooo.     .oooooo.     .oooooo.    ooooooooo.         .o.       ooo        ooooo    #####
#####    `888   `Y88. `888   `Y88.  d8P'  `Y8b   d8P'  `Y8b   `888   `Y88.      .888.      `88.       .888'    #####
#####     888   .d88'  888   .d88' 888      888 888            888   .d88'     .8"888.      888b     d'888     #####
#####     888ooo88P'   888ooo88P'  888      888 888            888ooo88P'     .8' `888.     8 Y88. .P  888     #####
#####     888          888`88b.    888      888 888     ooooo  888`88b.      .88ooo8888.    8  `888'   888     #####
#####     888          888  `88b.  `88b    d88' `88.    .88'   888  `88b.   .8'     `888.   8    Y     888     #####
#####    o888o        o888o  o888o  `Y8bood8P'   `Y8bood8P'   o888o  o888o o88o     o8888o o8o        o888o    #####
#####                                                                                                          #####
####################################################################################################################
####################################################################################################################
#####                 ________________________________________________________________________                 ##### 
#####________________|     This is a sample program that gets some data from a recipe api     |________________#####
#####‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾|just to show a potential feature that could be added to this application|‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾#####
#####                 ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾                 ##### 
####################################################################################################################
####################################################################################################################

from random import random
from time import sleep
import requests
import json

def showIngredientsForRecipe(id):
    url = "https://tasty.p.rapidapi.com/recipes/get-more-info"

    querystring = {"id": id}

    headers = {
        "X-RapidAPI-Key": "93b021b6f3msh30cbc417c385c2ap1c9d98jsn75d8ddb84636",
        "X-RapidAPI-Host": "tasty.p.rapidapi.com"
    }
    resp = requests.request("GET", url, headers=headers, params=querystring)
    file = open("recipeResponse.json", "w")
    file.write(json.dumps(resp.json(), indent = 2))
    file = open("recipeResponse.json","r")
    recipeArray = json.loads(file.read())
    componentList = recipeArray["sections"][0]["components"]
    ingredientList = []
    print("Dish:",recipeArray["name"])
    sleep(0.5)
    for i in range(len(componentList)):
        ingredientList.append(componentList[i]["ingredient"]["name"])
        print(f"Ingredient #{i+1}:",componentList[i]["raw_text"])
        sleep(0.2)
    

def makeTags():
    url = "https://tasty.p.rapidapi.com/tags/list"

    headers = {
	    "X-RapidAPI-Key": "93b021b6f3msh30cbc417c385c2ap1c9d98jsn75d8ddb84636",
	    "X-RapidAPI-Host": "tasty.p.rapidapi.com"
    }
    resp = requests.request("GET", url, headers=headers)
    file = open("tagList.json", "w")
    file.write(json.dumps(resp.json(), indent = 2))
    file = open("tagList.json","r")
    recipeArray = json.loads(file.read())

def getAllRecipes():
    url = "https://tasty.p.rapidapi.com/recipes/list"

    querystring = {"from":"0","size":"20","tags":"under_30_minutes"}

    headers = {
        "X-RapidAPI-Key": "93b021b6f3msh30cbc417c385c2ap1c9d98jsn75d8ddb84636",
        "X-RapidAPI-Host": "tasty.p.rapidapi.com"
    }

    resp = requests.request("GET", url, headers=headers, params=querystring)
    file = open("allRecipes.json", "w")
    file.write(json.dumps(resp.json(), indent = 2))

makeTags()
getAllRecipes()
file = open("allRecipes.json","r")
recipeArray = json.loads(file.read())
count = recipeArray["count"]
recipeNumber = 0
id = recipeArray["results"][recipeNumber]["canonical_id"][7:]
showIngredientsForRecipe(id)