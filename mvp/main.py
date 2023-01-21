# main.py

from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/user_info/{user_id}/{user_request}")
async def user_info(user_id: int, user_request: str):
    model_url = "https://6dky2c4nx4.execute-api.us-east-1.amazonaws.com/default/openLineageWorker"
    model_payload = {
        "user_id": user_id,
        "text" : user_request
    }

    model_response = requests.request("POST", model_url, json=model_payload)
    content = model_response.json()
    {"user_id": 54,
      "user_class": "Experto en delivery",
        "most_spent": ["Jumbo", "Uber", "CamiloCorp", "SebaInc"],
                        "expected_next_spent": 100000, "rich_text": "En el a\u00f1o pasado esta ha sido tu historia:"}
    return {
        "user_id": user_id,
        "most_spent": content["most_spent"],
        "expected_spend" : content["expected_next_spent"],
        "prompt_responde": content["rich_text"]
    }

@app.get("/user_groups/{user_id}")
async def user_groups(user_id: int):
    return {
        "user_id": user_id,
        "data": {
        "user_group": "Hello World"} 
    }