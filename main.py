import os
import json
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from screener_engine import MultiTimeframeScreener
from seasonal_macro import SeasonalMacroEngine
from angel_broker import AngelOneMasterBroker

app = FastAPI(title="BharatAlgo Institutional Terminal", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

screener = MultiTimeframeScreener()
broker = AngelOneMasterBroker()

@app.on_event("startup")
async def startup():
    print("=========================================================")
    print("   BHARAT ALGO PRO - ANGEL ONE MASTER PRODUCTION ENGINE  ")
    print("=========================================================")
    broker.authenticate()

@app.get("/api/v1/auth/callback")
async def smartapi_callback(auth_token: str = None):
    """Satisfies Angel One requirement for valid HTTPS Redirect URL."""
    return {"status": "SUCCESS", "message": "Angel One Authentication Token captured", "token": auth_token}

@app.post("/api/v1/orders/postback")
async def smartapi_postback(payload: dict):
    """Satisfies Angel One requirement for valid HTTPS Postback URL."""
    print(f"[POSTBACK UPDATE]: {payload}")
    return {"status": "ACK"}

@app.get("/api/v1/signals/intraday")
async def get_intraday_signals():
    return screener.analyze_intraday()

@app.get("/api/v1/signals/swing")
async def get_swing_signals():
    return screener.analyze_swing()

@app.get("/api/v1/signals/longterm")
async def get_longterm_signals():
    return screener.analyze_longterm()

@app.get("/api/v1/signals/derivatives")
async def get_derivatives_signals():
    return screener.analyze_derivatives()

@app.get("/api/v1/macro")
async def get_macro():
    return SeasonalMacroEngine.get_global_news_sentiment()

@app.post("/api/v1/order/execute")
async def execute_order(req: dict):
    return broker.execute_order(
        symbol=req.get("symbol"),
        side=req.get("side"),
        qty=req.get("qty", 1),
        product=req.get("product", "INTRADAY")
    )

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
