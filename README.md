# Bubba Technologies Inc. Python Scraper
## Created by Matthew Groholski
## README Last Update: 08/02/23

### File Creation
Use scripts/fileBuilder.py to create JSON files with website scraping information.

##### Store Name
Trivial. (Ex: Lululemon)

##### Store URL
Homepage URL for the store. (Ex: https://shop.lululemon.com)

#### Catalog Page Information
##### Catalog Regex
1. Enter the amount of unique catalog URL routes.
2. For each unique route, enter REGEX to identify. (Ex. https://shop.lululemon.com/c/mens-jackets-and-outerwear/_/N-8rm should be /c/[^_]+)

##### Catalog API
**Only use if the store uses an API to load catalog clothing.**
###### Catalog API Encoding
Input URL to get API information. Replace any category specific parameters with regex[x][y] where x is the regex expression index (zero indexed) and y is the group within the regex expression.

###### Product Route
**See section about JSON Parsing for route formatting.**
Input route to find product URLs. 

#### Product Page Information
##### Product Regex
1. Enter the amount of unique product URL routes.
2. For each unique route, enter REGEX to identify. (Ex. https://shop.lululemon.com/p/women-tanks/Ribbed-Softstreme-Cropped-Tank-Top/_/prod11460279?color=35955 should be /p/.+)

##### Product API
**Only use if the store uses an API to load product information.**
###### Product API Encoding
Input URL to get API information. The product URL will be disected into three parts: {baseUrl}, {route}, {parameters}. Format accordingly.

Example:
Product URL: https://shop.lululemon.com/p/women-tanks/Ribbed-Softstreme-Cropped-Tank-Top/_/prod11460279?color=35955
API URL: https://shop.lululemon.com/api/p/women-tanks/Ribbed-Softstreme-Cropped-Tank-Top/_/prod11460279
API URL Encoding: {baseUrl}/api{route}

###### Name Route
**See section about JSON Parsing for route formatting.**
Input route to find product name within the JSON response.

###### Image Route
**See section about JSON Parsing for route formatting.**
Input route to find the product images within the JSON response.

###### Gender
**Specific Gender**
If the store only carries clothing for a specific gender input the corresponding gender: Male, Female, Kid, Girl, Boy, Unisex.

**Gender Route**
**See section about JSON Parsing for route formatting.**
Input route to find product gender within the JSON response.

###### Clothing Description
**Route**
**See section about JSON Parsing for route formatting.**
Input route to find the product description within the JSON response.

**Regex**
Following prompts to enter store specific regex to create tags for clothing.

#### JSON Route Formatting
##### Operators
Enter all operators after the tag inside brackets ([]) to search through children. If a URL parameter is needed, use {param:x} with x as the parameter name.
**Equal To (=)**
Gets all children with an attribute equal to the value set.
Example: [color-code={param:color}]
**Not Equal To (!=)**
Gets all children with an attribute not equal to the value set.
Example: [color-code!={param:color}]
**Greater Than (>)**
Gets all children with an attribute greater than the value set.
Example: [color-code>{param:color}]
**Greater Than or Equal To (>=)**
Gets all children with an attribute greater than or equal to the value set.
Example: [color-code>={param:color}]
**Less Than (<)**
Gets all children with an attribute greater than the value set.
Example: [color-code<{param:color}]
**Less Than or Equal To (<=)**
Gets all children with an attribute greater than or equal to the value set.
Example: [color-code<={param:color}]
**All (*)**
Gets all children.
Example: [*]

### Main

### Scraper Tools

