import os

#Scraper Settings
SCRAPER_TIMEOUT_SECONDS = 30
SLEEP_FLOOR_SECONDS = 2
SLEEP_CEIL_SECONDS = 10

#API Settings
API_URL = "https://api.peachsconemarket.com"
API_LOGIN_DATA = {
        "username": os.getenv("PEACHSCONE_API_USERNAME", "scraper-server"),
        "password": os.getenv("PEACHSCONE_API_PASSWORD", "rycsef-Wofny9")
    }

#Proxy Settings
PROXY = {
    "http":f"http://customer-{os.getenv('PROXY_USERNAME')}:{os.getenv('PROXY_PASSWORD')}@us-pr.oxylabs.io:10000",
    "https":f"http://customer-{os.getenv('PROXY_USERNAME')}:{os.getenv('PROXY_PASSWORD')}@us-pr.oxylabs.io:10000"
}