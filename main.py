from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI()

class Question(BaseModel):
    query: str

@app.post("/ask")
async def ask(question: Question):
    key = os.getenv("OPENROUTER_API_KEY")
    if not key:
        return {"error": "API Key fehlt. Setze OPENROUTER_API_KEY in Render."}

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "meta-llama/llama-3-8b-instruct:nitro",
        "messages": [
            {"role": "system", "content": "Du bist ein smarter Sprachassistent."},
            {"role": "user", "content": question.query}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    result = response.json()

    try:
        reply = result["choices"][0]["message"]["content"]
    except:
        reply = "Fehler bei der Antwort: " + str(result)

    return {"response": reply}
