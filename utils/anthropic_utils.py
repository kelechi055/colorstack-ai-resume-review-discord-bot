import json
from config import ANTHROPIC_API_KEY
import requests
import logging
import asyncio

# Function to Get Chat Completion from Anthropic
def get_chat_completion(max_tokens: int, messages: list, system: str = None, temperature: float = 0.5) -> str:
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        'Content-Type': 'application/json',
        'anthropic-version': '2023-06-01',
        'x-api-key': ANTHROPIC_API_KEY,
    }
    data = {
        'messages': messages,
        'model': 'claude-3-5-sonnet-20240620',
        'max_tokens': max_tokens,
        'temperature': temperature,
    }
    if system:
        data['system'] = system

    retries = 3
    for attempt in range(retries):
        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            response.raise_for_status()
            return response.text
        except (requests.HTTPError, ConnectionError, requests.RequestException, ValueError) as err:
            logging.error("Error during API request attempt %d: %s", attempt + 1, err)
            if attempt < retries - 1:
                logging.info("Retrying...")
                asyncio.sleep(2)
            else:
                logging.error("Failed after %d attempts", retries)
                raise
    
    if not response.ok:
        logging.error(f"Failed to fetch chat completion from Anthropic. Status: {response.status_code}, Response: {response.text}")
        raise Exception(f"Failed to fetch chat completion from Anthropic. Status: {response.status_code}, Response: {response.text}")

    json_response = response.json()
    logging.info("Received chat completion from Anthropic successfully")
    return json_response.get('completion', '').strip()