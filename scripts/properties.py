import os

#Scraper Settings
SCRAPER_TIMEOUT_SECONDS = 30
SLEEP_FLOOR_SECONDS = 2
SLEEP_CEIL_SECONDS = 10
IMAGE_WIDTH_PIXELS = 750
PRODUCT_PERCENTAGE = 0.60

#SCHEDULER SETTINGS
INFO_PATH = "./info"
OUTPUT_PATH = "./output"
SCRAPER_GROUP_MAX_AMOUNT = 3
MAX_PERCENTAGE = 1/3

#API Settings
API_URL = "https://api.peachsconemarket.com"
API_LOGIN_DATA = {
        "username": os.getenv("PEACHSCONE_API_USERNAME"),
        "password": os.getenv("PEACHSCONE_API_PASSWORD")
    }
API_HEADERS = {
        "Accept-Encoding": "gzip, deflate, br",
        "User-Agent": "Scraper Server - Python Requests",
        "Connection": "keep-alive",
        "Host": API_URL[8:]
    }

#Proxy Settings
PROXY = {
    "http":f"http://customer-{os.getenv('PROXY_USERNAME')}:{os.getenv('PROXY_PASSWORD')}@us-pr.oxylabs.io:10000",
    "https":f"http://customer-{os.getenv('PROXY_USERNAME')}:{os.getenv('PROXY_PASSWORD')}@us-pr.oxylabs.io:10000"
}