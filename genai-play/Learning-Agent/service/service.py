# service.py for Learning-Agent service module
import requests
from settings import Settings
from logger import logger

settings = Settings()

def get_greeting(name: str) -> str:
    return f"Hello, {name}! Welcome to the Learning-Agent service."

def get_user(user_id):
    logger.info(f"Fetching user data for user_id: {user_id}")
    logger.info(f"Requesting URL: user?id={user_id}")
    
    response = requests.get(f"http://backend:8001/user?id={user_id}")
    logger.info(f"Response Status Code: {response.json()}")
    if response.status_code == 200:
        return response.json()
    return {"error": "User not found"}

def get_portfolio(user_id):
    logger.info(f"Fetching portfolio for user_id: {user_id}")
    response = requests.get(f"http://backend:8001/portfolio?id={user_id}")
    logger.info(f"Response Status Code: {response.json()}")
    if response.status_code == 200:
        return response.json()
    return {"error": "Portfolio not found"}

def get_resource_categories():
    logger.info("Fetching resource categories")
    response = requests.get(f"http://backend:8001/resource_categories")
    logger.info(f"Response Status Code: {response.json()}")
    if response.status_code == 200:
        return response.json()
    return {"error": "Could not fetch resource categories"}

def get_resources_by_category(category):
    logger.info(f"Fetching resources for category: {category}")
    response = requests.get(f"http://backend:8001/resources?category={category}")
    logger.info(f"Response Status Code: {response.json()}")
    if response.status_code == 200:
        return response.json()
    return {"error": "Could not fetch resources for the given category"}


def invokellm(payload):
    
    logger.info(f"Invoking LLM with payload: {payload}")
    response = requests.post("http://litellm:4000/v1/chat/completions", 
                            headers={"Content-Type": "application/json", "Authorization": f"Bearer {settings.API_KEY}"},
                            json=payload
                            )
    
    logger.info(f"LLM Invocation Response: {response.json()}")
    if response.status_code == 200:
        return response.json()
    return {"error": "Could not connect to litellm server"}