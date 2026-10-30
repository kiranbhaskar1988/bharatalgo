import json
import pyotp
try:
    from SmartApi import SmartConnect
except ImportError:
    SmartConnect = None

class AngelOneMasterBroker:
    def __init__(self, config_path="config.json"):
        with open(config_path) as f:
            self.cfg = json.load(f)
        self.api = None

    def authenticate(self):
        if self.cfg.get("paper_trading", True):
            print("[PAPER TRADING MODE]: Authenticated with Virtual Angel One Execution Terminal.")
            return True

        if not SmartConnect:
            raise ImportError("Please install 'smartapi-python' using 'pip install smartapi-python'")

        self.api = SmartConnect(self.cfg["api_key"])
        totp = pyotp.TOTP(self.cfg["totp_secret"]).now()
        res = self.api.generateSession(self.cfg["client_code"], self.cfg["pin"], totp)
        if res.get("status"):
            print(f"[ANGEL ONE LIVE]: Successfully authenticated for Client Code: {self.cfg['client_code']}")
            return True
        raise ConnectionError(f"SmartAPI login failed: {res.get('message')}")

    def execute_order(self, symbol: str, side: str, qty: int = 1, product: str = "INTRADAY"):
        if self.cfg.get("paper_trading", True):
            print(f"[PAPER ORDER EXECUTED]: {side} {qty} shares of {symbol} ({product})")
            return {"status": "SUCCESS", "mode": "PAPER", "symbol": symbol, "order_id": "SIM_998811"}

        params = {
            "variety": "NORMAL",
            "tradingsymbol": symbol,
            "symboltoken": "3045",
            "transactiontype": side,
            "exchange": "NFO" if ("CE" in symbol or "PE" in symbol or "FUT" in symbol) else "NSE",
            "ordertype": "MARKET",
            "producttype": product,
            "duration": "DAY",
            "quantity": str(qty)
        }
        return self.api.placeOrder(params)
