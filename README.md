# Bubba Technologies Inc. Python Scraper
## Created by Matthew Groholski
### README Last Update: 05/13/23

Use scripts/fileBuilder.py to create JSON files with website scraping information.

### **API**
#### **API URL**
The url will be boken up into two parts basicUrl and route. To provide the api url use {baseUrl} and {route} to provide the structure.

Example: https://shop.lululemon.com/p/womens-sweatpants/Softstreme-HR-Straight-Leg-Crop/_/prod11020342

apiUrl:{baseUrl}/api{route}

baseUrl: https://shop.lululemon.com

route: /p/womens-sweatpants/Softstreme-HR-Straight-Leg-Crop/_/prod11020342

apiUrl: https://shop.lululemon.com/api/p/womens-sweatpants/Softstreme-HR-Straight-Leg-Crop/_/prod11020342

#### **JSON Tag Identifier**
Provide the structure to find json tag. * is a wildcard to access an JSON array.
