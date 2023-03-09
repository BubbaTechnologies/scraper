#Matthew Groholski
#Feburary 4th, 2023

import json
import scrapertools
import re

def main():
    scrapertools.cdFile(__file__)

    data = {}

    #Gets input
    data["name"] = input("Store Name: ")
    data["url"] = input("Store URL: ")

    #Checks url input
    urlCheck = re.fullmatch("https://(www|shop)\..+\.(com|co)", data["url"])
    if not urlCheck:
        raise ValueError("Invalid URL address format.")

    data["webpageRegex"] = []
    count = int(input("Webpage Regex Count: "))

    for i in range(0, count):
        regex = input("Webpage Regex " + str(i + 1) + ": ")
        data["webpageRegex"].append(regex)

    data["clothingRegex"] = []
    count = int(input("Clothing Page Regex Count: "))

    for i in range(0, count):
        regex = input("Clothing Page Regex " + str(i + 1) + ": ")
        data["clothingRegex"].append(regex)
    
    data["nameIdentifier"] = input("Name Identifier: ")
    data["imageIdentifier"] = input("Image Div Identifier: ")

    if input("Are there breadcrumbs? (Yes/No) ").lower() == "yes":
        data["breadcrumbsIdentifier"] = input("Breadcrumbs Identifier: ")
    elif input("Is there a specific gender? (Yes/No) ").lower() == "yes":
        data["gender"] = input("Gender: (Male/Female/Boy/Girl) ").lower()
        if data["gender"] not in ["male", "female", "boy", "girl"]:
            data["gender"] = "other";

    with open("../info/" + data["name"].lower() + ".json", 'w') as file:
        print("Writing file " + scrapertools.pwd() + data["name"] + ".json")
        json.dump(data, file)


if __name__ == "__main__":
    main()