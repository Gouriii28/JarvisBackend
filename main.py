from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import json
import httpx
from datetime import datetime

app = FastAPI(title="JARVIS Backend", version="1.0.0")

# ── CORS — allow ALL origins (fixes browser blocking) ─────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Config ────────────────────────────────────────────────────────────────────
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_URL     = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL   = "llama3-8b-8192"

JARVIS_SYSTEM = """You are JARVIS — Joint Artificially Responsive Virtual Intelligence System.
You are a highly advanced AI assistant with a sleek, professional, slightly witty personality.
Keep responses concise and intelligent. Occasionally address the user as 'boss'.
Use technical-sounding language where appropriate. Never break character."""

# ── Models ────────────────────────────────────────────────────────────────────
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Message]] = []

# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"status": "online", "system": "JARVIS", "version": "1.0.0"}

@app.get("/health")
def health():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

@app.post("/chat")
async def chat(req: ChatRequest):
    if not GROQ_API_KEY:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY not configured on server.")

    messages = [{"role": "system", "content": JARVIS_SYSTEM}]
    for m in req.history:
        messages.append({"role": m.role, "content": m.content})
    messages.append({"role": "user", "content": req.message})

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                GROQ_URL,
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={"model": GROQ_MODEL, "messages": messages, "max_tokens": 1024},
            )

        print("GROQ RESPONSE:", resp.text)

        if resp.status_code != 200:
            raise HTTPException(status_code=502, detail=f"Groq API error: {resp.text}")

        reply = resp.json()["choices"][0]["message"]["content"]
        return {"reply": reply, "timestamp": datetime.utcnow().isoformat()}

    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Request to Groq timed out.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
