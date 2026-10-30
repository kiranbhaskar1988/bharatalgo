import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="BharatAlgo Production Terminal")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/")
def home():
    return {"status": "ONLINE", "message": "BharatAlgo Master Suite running successfully on Render!"}

@app.get("/api/v1/auth/callback")
def callback(auth_token: str = None):
    return {"status": "SUCCESS", "token": auth_token}

@app.post("/api/v1/orders/postback")
def postback(payload: dict):
    return {"status": "ACK"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))