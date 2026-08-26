import requests

from app.config import settings

HF_API_URL = "https://router.huggingface.co/hf-inference/models/sentence-transformers/all-MiniLM-L6-v2/pipeline/feature-extraction"


def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Convert a list of text chunks into embedding vectors via
    HuggingFace's hosted router API.
    """
    headers = {"Authorization": f"Bearer {settings.huggingface_api_key}"}

    response = requests.post(
        HF_API_URL,
        headers=headers,
        json={"inputs": texts, "options": {"wait_for_model": True}},
        timeout=30,
    )
    response.raise_for_status()

    return response.json()
