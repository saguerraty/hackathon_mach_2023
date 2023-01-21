# main.py

from fastapi import FastAPI

app = FastAPI()

@app.get("/user_info/{user_id}")
async def user_info(user_id: int):
    return {
        "user_id": user_id,
        "data": {
        "user_avg_spend": 100,
        }
        }

@app.get("/user_groups/{user_id}")
async def user_groups(user_id: int):
    return {
        "user_id": user_id,
        "data": {
        "user_group": "Hello World"} 
    }

@app.get("/user_spend/{user_id}")
async def user_spend(user_id: int):
    return {"user_id": user_id, "data": {"user_total_spend": 100}}