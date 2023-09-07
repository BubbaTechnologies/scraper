#Matthew Groholski
#July 22nd, 2023

import json
import scrapertools
import re
from typing import List


def checkGender(inp: str)->str:
    if inp not in ["male", "female", "boy", "girl"]:
        return "other"
    return inp

def getTagRegex()->List[str]:
    regex = {}
    if input("Use default clothing tag regex? (Yes/No) ").lower() == "no":
        print("Please see README.md tags section for information about formatting.")
        for i in scrapertools.TAG_DICT.keys():
            regex[i] = []
            for i in range(int(input(f"Regex count for {i}: "))):
                regex[i].append(input(f"{i} Regex " + str(i + 1) + ": "))
        return regex

def main():
    try:
        scrapertools.cdFile(__file__)

        data = {}

        #Gets input
        data["name"] = input("Store Name: ")
        data["url"] = input("Store URL: ")

        #Checks url input
        urlCheck = re.fullmatch("http(?:s)?://(?:(?:www|shop)\.)?.+\.(?:com|co|co\.uk)", data["url"])
        if not urlCheck:
            raise ValueError("Invalid URL address format.")
        
        data["loadJavascript"] = input("Load Javascript? (Yes/No) ").lower() == "yes"
        
        catalogInformationKey = "catalogPageInformation"
        data[catalogInformationKey] = {
            "regex": []
            }
        count = int(input("Catalog Regex Count: "))

        for i in range(0, count):
            data[catalogInformationKey]["regex"].append(input("Catalog Regex " + str(i + 1) + ": "))

        data[catalogInformationKey]["api"] = None
        if input("Is there a catalog page API? (Yes/No) ").lower() == "yes":
            data[catalogInformationKey]["api"] = {}
            print("See README.md for instructions on how to encode catalog page API url.")
            data[catalogInformationKey]["api"]["urlEncoding"] = input("Catalog API Url Encoding: ")
            print("See README.md for instructions on how to encode product url for catalog API's.")
            data[catalogInformationKey]["api"]["productUrl"] = input("Product Url: ")


        productInfromationKey = "productPageInformation"
        data[productInfromationKey] = {}
        data[productInfromationKey]["regex"] = []
        for i in range(0, int(input("Product Page Regex Count: "))):
            data[productInfromationKey]["regex"].append(input("Product Page Regex " + str(i + 1) + ": "))
        
        if input("Is there an product page API? (Yes/No) ").lower() == "yes":
            data[productInfromationKey]["api"] = {}
            print("See README.md for instructions on how to encode product page API url.")
            data[productInfromationKey]["api"]["apiUrlEncoding"] = input("API Url Encoding: ")
            data[productInfromationKey]["api"]["nameRoute"] = input("Name Route: ")
            data[productInfromationKey]["api"]["imageRoute"] = input("Image Route: ")
            # if input("Is there a featured image? (Yes/No) ").lower() == "yes":
            #     data[productInfromationKey]["api"]["featuredImageRoute"] = input("Featured Image Route: ")

            if input("Is there a specific gender? (Yes/No) ").lower() == "yes":
                data[productInfromationKey]["api"]["gender"] = checkGender(input("Gender: (Male/Female/Boy/Girl) ").lower())
            else:
                data[productInfromationKey]["api"]["genderRoute"] = input("Gender Route: ")
        else:
            data[productInfromationKey]["identifiers"] = {}
            data[productInfromationKey]["identifiers"]["nameIdentifier"] = input("Name Identifier: ")
            data[productInfromationKey]["identifiers"]["imageDivIdentifier"] = input("Image Div Identifier: ")

            if input("Are there breadcrumbs? (Yes/No) ").lower() == "yes":
                data[productInfromationKey]["identifiers"]["breadcrumbsIdentifier"] = input("Breadcrumbs Identifier: ")
            elif input("Is there a specific gender? (Yes/No) ").lower() == "yes":
                data[productInfromationKey]["identifiers"]["gender"] = checkGender(input("Gender: (Male/Female/Boy/Girl) ").lower())

        if "api" in data[productInfromationKey].keys():
            data[productInfromationKey]["api"]["clothingDescription"] = {"route": input("Clothing Description Route: ")}
            data[productInfromationKey]["api"]["clothingDescription"]["regex"] = getTagRegex()
        else:
            data[productInfromationKey]["identifiers"]["clothingDescription"] = {"divIdentifier": input("Clothing Description Div Identifier: ")}
            data[productInfromationKey]["identifiers"]["clothingDescription"]["regex"] = getTagRegex()

        with open(f"../info/" + data["name"].lower().replace(" ","_") + ".json", 'w') as file:
            print("Writing file " + scrapertools.pwd() + "/" + data["name"].lower().replace(" ","_") + ".json")
            json.dump(data, file)
    except Exception as e:
        print("Error: " + str(e))


if __name__ == "__main__":
    main()