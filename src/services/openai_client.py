from openai import OpenAI
from services.config_loader import config_loader

def create_openai_client():
    return OpenAI(api_key=config_loader.openai_api_key)

client = create_openai_client()
