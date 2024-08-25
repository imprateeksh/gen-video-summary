import requests

URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral" # "llama3.1"
ROLE = "user"

def get_results(query: str) -> str:
    """Get response using OLLAMA API."""
    data = {
        "model": MODEL_NAME,
        "prompt": query,
        "stream": False
    }
    try:
        result = requests.post(url=URL, json=data)
        result.raise_for_status()
        return result.json().get("response")
    except requests.exceptions.RequestException as ex:
        raise ValueError(f"Error occurred as : \n {ex}")
