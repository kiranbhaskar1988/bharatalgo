import datetime
import yfinance as yf
import feedparser
from textblob import TextBlob

class SeasonalMacroEngine:
    """Calculates Seasonal Calendar, Brent Crude Impact & Global News Sentiment."""
    
    @staticmethod
    def get_seasonal_factor() -> float:
        today = datetime.date.today()
        month, day = today.month, today.day
        if month in [10, 11]:   # Pre-Diwali / Festive Rally
            return 1.20
        elif month == 1:        # Pre-Union Budget Rally
            return 1.15
        elif month == 3 and day > 20: # March Fiscal Year End
            return 0.85
        return 1.00

    @staticmethod
    def get_global_news_sentiment() -> dict:
        sentiment_score = 0.0
        crude_impact = "NEUTRAL"
        try:
            crude = yf.Ticker("BZ=F").history(period="2d")
            if len(crude) >= 2:
                pct = ((crude['Close'].iloc[-1] - crude['Close'].iloc[-2]) / crude['Close'].iloc[-2]) * 100
                if pct > 1.5:
                    sentiment_score -= 15.0
                    crude_impact = "BEARISH (Crude Spiked)"
                elif pct < -1.5:
                    sentiment_score += 15.0
                    crude_impact = "BULLISH (Crude Softened)"

            # Parse ET Financial Feeds
            url = "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms"
            feed = feedparser.parse(url)
            polarities = [TextBlob(e.title).sentiment.polarity for e in feed.entries[:6]]
            if polarities:
                sentiment_score += (sum(polarities) / len(polarities)) * 40.0
        except Exception as e:
            print(f"[MACRO WARNING]: {e}")

        return {
            "score": round(max(min(sentiment_score, 100), -100), 2),
            "crude_status": crude_impact,
            "seasonal_multiplier": SeasonalMacroEngine.get_seasonal_factor()
        }
