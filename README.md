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

###### Product Url
**See section about JSON Parsing for route formatting.**
Input product url format with JSON Parsing in brackets where needed.
Example:
Product Url:
```
https://vuoriclothing.com/products/{products[*]/product-id}
```
Api Json Response:
```
{
    "products": [
        {
            "product_id": "womens-third-eye-muscle-tank-black",
            "title": "Third Eye Muscle Tank | Black",
            "description": "\u003cspan\u003eGraphic with a muscle-tank fit, the women's Third Eye Muscle Tank features a simple eye graphic on the front with a classic cotton feel. Great for yoga, training, hiking and chilling.\u003c\/span\u003e",
            "brand": "Vuori Clothing",
            "offers": [
                {
                    "title": "Black \/ XS",
                    "offer_id": 22963966476346,
                    "sku": "VW937BLKXSM",
                    "price": 22.0,
                    "currency_code": "USD",
                    "in_stock": false
                },
                {
                    "title": "Black \/ S",
                    "offer_id": 22963966509114,
                    "sku": "VW937BLKSML",
                    "price": 22.0,
                    "currency_code": "USD",
                    "in_stock": false
                },
                {
                    "title": "Black \/ M",
                    "offer_id": 22963966541882,
                    "sku": "VW937BLKMED",
                    "price": 22.0,
                    "currency_code": "USD",
                    "in_stock": false
                },
                {
                    "title": "Black \/ L",
                    "offer_id": 22963966574650,
                    "sku": "VW937BLKLRG",
                    "price": 22.0,
                    "currency_code": "USD",
                    "in_stock": false
                },
                {
                    "title": "Black \/ XL",
                    "offer_id": 22963966607418,
                    "sku": "VW937BLKXLG",
                    "price": 22.0,
                    "currency_code": "USD",
                    "in_stock": false
                }
            ],
            "thumbnail_url": "\/\/cdn.shopify.com\/s\/files\/1\/0022\/4008\/6074\/products\/VW937BLK_1.jpg?v=1556580999"
        },
        {
            "product_id": "womens-best-day-crop-white",
            "title": "Best Day Crop | White",
            "description": "\u003cspan\u003eGraphic with a cropped tank fit, the women's Best Day Crop features a sunset graphic on the front with a classic cotton feel. Great for yoga, training, hiking and chilling.\u003c\/span\u003e",
            "brand": "Vuori Clothing",
            "offers": [
                {
                    "title": "White \/ XS",
                    "offer_id": 22963966640186,
                    "sku": "VW936WHTXSM",
                    "price": 14.0,
                    "currency_code": "USD",
                    "in_stock": false
                },
                {
                    "title": "White \/ S",
                    "offer_id": 22963966672954,
                    "sku": "VW936WHTSML",
                    "price": 14.0,
                    "currency_code": "USD",
                    "in_stock": false
                },
                {
                    "title": "White \/ M",
                    "offer_id": 22963966705722,
                    "sku": "VW936WHTMED",
                    "price": 14.0,
                    "currency_code": "USD",
                    "in_stock": false
                },
                {
                    "title": "White \/ L",
                    "offer_id": 22963966738490,
                    "sku": "VW936WHTLRG",
                    "price": 14.0,
                    "currency_code": "USD",
                    "in_stock": false
                },
                {
                    "title": "White \/ XL",
                    "offer_id": 22963966771258,
                    "sku": "VW936WHTXLG",
                    "price": 14.0,
                    "currency_code": "USD",
                    "in_stock": false
                }
            ],
            "thumbnail_url": "\/\/cdn.shopify.com\/s\/files\/1\/0022\/4008\/6074\/products\/VW936WHT_new1.jpg?v=1556580829"
        }
    ]
}
```

Result:
```
["https://vuoriclothing.com/products/womens-third-eye-muscle-tank-black","https://vuoriclothing.com/products/womens-best-day-crop-white"]
```
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

