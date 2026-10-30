# BharatAlgo Pro - Master Production Suite

Comprehensive Algorithmic Trading Terminal for Indian Equities, Futures & Options (NSE / BSE / NFO).

## Included Engines & Requirements:
1. **Free Angel One SmartAPI Bridge**: Auto 2FA TOTP login using `pyotp`, zero recurring API costs.
2. **Dynamic Nifty 200 Scanner**: Scans expandable NSE universes (Nifty 50, Nifty 100, Nifty 200).
3. **4 Operational Windows**:
   - **Intraday Window**: 15-min timeframe Buy Calls vs Short Calls.
   - **Swing Window**: Multi-day Golden Cross & Sector Outperformers.
   - **Long-Term Window**: Fundamental wealth creation (ROCE > 20%, low debt, 3Y profit growth).
   - **Derivatives Desk**: Nifty & BankNifty ATM/OTM Option strike selector & Stock Futures OI build-up.
4. **Seasonal & Global Macro Engine**: Evaluates Diwali/Budget calendar factors, Brent Crude oil, US 10Y yields, and RSS news sentiment.
5. **1-Click Deployment (Render.com / GitHub)**: Includes `render.yaml` and FastAPI callback endpoints for Angel One HTTPS URL validation.

## Deployment Instructions:
1. Push this unzipped folder to GitHub.
2. Connect the repo to **Render.com** (Web Service). Render automatically uses `render.yaml`.
3. Set your live Render HTTPS URL in Angel One SmartAPI Developer Portal:
   - **Redirect URL**: `https://your-service.onrender.com/api/v1/auth/callback`
   - **Postback URL**: `https://your-service.onrender.com/api/v1/orders/postback`
