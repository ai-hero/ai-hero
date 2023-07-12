import os

import httpx

BASE_URL = "https://api.openai.com/v1/"
COMPLETIONS = "completions"
MODEL = "text-davinci-003"
EMBEDDINGS = "embeddings"
EMBEDDINGS_MODEL = "text-embedding-ada-002"
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


def has_key():
    return OPENAI_API_KEY is not None


def complete_with_gpt3(row: dict, template: any, api_key: str = OPENAI_API_KEY):
    prompt = template.render(**row)
    try:
        with httpx.Client(
            base_url=BASE_URL,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
        ) as client:
            resp = client.post(
                COMPLETIONS,
                json={"model": MODEL, "prompt": prompt, "max_tokens": 512},
                timeout=30,
            )
            resp.raise_for_status()
            prediction_object = resp.json()
            if "errors" in prediction_object:
                return None, prediction_object["errors"][0]["text"].strip()
            else:
                completion = prediction_object["choices"][0]["text"].strip()
                print(f"Prompt:{prompt}\nCompletion:{completion}")
                return completion, None
    except httpx.HTTPError as e:
        return None, str(e)


def get_embedding(text: str, api_key: str = OPENAI_API_KEY):
    try:
        with httpx.Client(
            base_url=BASE_URL,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
        ) as client:
            resp = client.post(
                EMBEDDINGS,
                json={"model": EMBEDDINGS_MODEL, "input": text},
                timeout=30,
            )
            resp.raise_for_status()
            prediction_object = resp.json()
            if "errors" in prediction_object:
                return None, prediction_object["errors"][0]["text"].strip()
            else:
                embedding = prediction_object["data"][0]["embedding"]
                return embedding, None
    except httpx.HTTPError as http_error:
        return None, str(http_error)
