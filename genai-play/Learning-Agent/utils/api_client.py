import requests
from settings import Settings

settings = Settings()

def get_user_data(user_id):
    """Fetch user data from the external API."""
    response = requests.get(f"{user_id}")
    if response.status_code == 200:
        return response.json()
    return None