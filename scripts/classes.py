import requests
from scrapertools import printMessage
import properties
from typing import Dict
from enum import Enum

class Api:
    '''
        A class holding the API information needed to run the script.
    '''
    def __init__(self):
        self.__JWT = ""
        self.__login()

    def __login(self):
        #TODO: Remove
        return
        loginResponse = requests.post(properties.API_URL + "/login", headers={"Content-Type":"application/json"}, json = properties.API_LOGIN_DATA)
        if loginResponse.status_code != 200:
            printMessage(f"Received code {loginResponse.status_code} from API.")
            exit()
        self.__JWT = loginResponse.json()["jwt"]
        
    def __str__(self):
        return str({"jwt": self.__JWT})
    
    def getJwt(self):
        return self.__JWT
    
class Relation(Enum):
    '''
        I documented this too late. I think it has something to do with parsing the json.
    '''
    EQUAL="="
    NOT_EQUAL="!="
    LESS_THAN="<"
    LESS_THAN_OR_EQUAL="<="
    GREATER_THAN=">"
    GREATER_THAN_OR_EQUAL=">="
    
    def compute(self, a, b)->bool:
        if type(a) != type(b):
            raise TypeError("Cannot compare two different types.")
        
        match self:
            case Relation.EQUAL:
                return (a==b)
            case Relation.NOT_EQUAL:
                return (a!=b)
            case Relation.LESS_THAN:
                return (a<b)
            case Relation.LESS_THAN_OR_EQUAL:
                return (a<=b)
            case Relation.GREATER_THAN:
                return (a>b)
            case Relation.GREATER_THAN_OR_EQUAL:
                return (a>=b)

class Clothing:
    def __init__(self, name: str, imageUrl: list[str], productUrl: str, type: str, gender: str, tags: list[str]):
        self.name = name
        self.imageUrl = imageUrl
        self.productUrl = productUrl
        self.storeId: int = None
        self.type = type
        self.gender = gender
        self.tags = tags

    def toDict(self):
        dictObj = {
            "name": self.name,
            "imageUrl": self.imageUrl,
            "productUrl": self.productUrl,
            "storeId": str(self.storeId),
            "type": self.type,
            "gender": self.gender,
            "tags": self.tags
        }

        return dictObj

    def __str__(self):
        return str(self.toDict())

    def createClothing(self, jwt):
        #TODO: Remove
        return
        
        header = {
            "Authorization": "Bearer " + jwt,
            "Content-Type": "application/json"
        }

        response = requests.post(properties.API_URL + "/scraper/clothing", headers=header, json=self.toDict())
        try:
            return response.json()["id"]
        except KeyError:
            printMessage("Could not create clothing: " + str(response))
            return None
    
class Store:
    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url
        self.id = -1

    def toDict(self) -> Dict:
        dictObj = {
            "name": self.name,
            "url": self.url
        }

        return dictObj

    def __str__(self) -> str:
        return str(self.toDict())

    def createStore(self, jwt):
        #TODO: Remove
        return
        headers = {
            "Authorization": "Bearer " + jwt,
            "Content-Type": "application/json"
        }

        response = requests.post(url=properties.API_URL + "/scraper/store", headers=headers, json=self.toDict())
        try:
            self.id = response.json()["id"]
            return 
        except KeyError:
            printMessage("Could not create store: " + response)
            exit()