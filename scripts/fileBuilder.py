#Matthew Groholski
#Feburary 4th, 2023

import json
import scrapertools
import re
import os

def main():
    scrapertools.cdFile(__file__)

    groupNumber = input("Group Number: ")
    try:
        int(groupNumber)
    except:
        print("Invalid group number input.")
        exit()

    data = {}

    #Gets input
    data["name"] = input("Store Name: ")
    data["url"] = input("Store URL: ")

    #Checks url input
    urlCheck = re.fullmatch("http(s)?://((www|shop)\.)?.+\.(com|co)", data["url"])
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
    
    if input("Is there an API? (Yes/No) ").lower() == "yes":
        data["api"] = True
        data["apiUrlEncoding"] = input("API Url Encoding: ")
        data["nameKey"] = input("Name Key: ")
        data["imageKey"] = input("Image Key: ")
        if input("Is there a featured image? (Yes/No)").lower() == "yes":
            data["featuredImageKey"] = input("Featured Image Key: ")

        if input("Is there a specific gender? (Yes/No) ").lower() == "yes":
            data["gender"] = input("Gender: (Male/Female/Boy/Girl) ").lower()
            if data["gender"] not in ["male", "female", "boy", "girl"]:
                data["gender"] = "other"
        else:
            data["genderKey"] = input("Gender Key: ")
            if input("Is there tags? (Yes/No) ").lower() == "yes":
                data["tagsKey"] = input("Tags Key: ")
                if input("Is the type in tags? (Yes/No) ").lower() == "yes":
                    data["typeInTags"] = True
                else:
                    data["typeInTags"] = False
    else:
        data["api"] = False
        data["nameIdentifier"] = input("Name Identifier: ")
        data["imageIdentifier"] = input("Image Div Identifier: ")

        if input("Are there breadcrumbs? (Yes/No) ").lower() == "yes":
            data["breadcrumbsIdentifier"] = input("Breadcrumbs Identifier: ")
        elif input("Is there a specific gender? (Yes/No) ").lower() == "yes":
            data["gender"] = input("Gender: (Male/Female/Boy/Girl) ").lower()
            if data["gender"] not in ["male", "female", "boy", "girl"]:
                data["gender"] = "other"

    if not os.path.exists(f"../info/group{groupNumber}"):
        os.mkdir(f"../info/group{groupNumber}")
    
    with open(f"../info/group{groupNumber}/" + data["name"].lower().replace(" ","_") + ".json", 'w') as file:
        print("Writing file " + scrapertools.pwd() + "/" + data["name"].lower().replace(" ","_") + ".json")
        json.dump(data, file)


if __name__ == "__main__":
    main()