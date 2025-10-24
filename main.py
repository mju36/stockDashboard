from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, Dict, List
from datetime import datetime, timedelta
from decouple import config

from apiConn.alphaVantage import alphaVantage
from apiConn.polygonAPI import polygonAPI
from dataClasses.Ticker import Ticker
from dataClasses.OptionChain import OptionChain
from analysis.analytics import analytics

app = FastAPI(
    title="Stock Dashboard API",
    description="Real-time stock and options analytics API",
    version="1.0.0"
)

cache = {
    "tickers": {},
    "option_chains": {}
}

TICKER_CACHE_TTL = timedelta(seconds=30)
OPTION_CACHE_TTL = timedelta(minutes=1)

def get_cached_ticker(symbol: str) -> Optional[Ticker]:
    if symbol in cache["tickers"]:
        cached = cache["tickers"][symbol]
        if datetime.now() - cached["timestamp"] < TICKER_CACHE_TTL:
            return cached["data"]
    return None

def set_cached_ticker(symbol: str, ticker: Ticker):
    cache["tickers"][symbol] = {
        "data": ticker,
        "timestamp": datetime.now()
    }

def get_cached_option_chain(symbol: str, expiration: str) -> Optional[OptionChain]:
    cache_key = (symbol, expiration)
    if cache_key in cache["option_chains"]:
        cached = cache["option_chains"][cache_key]
        if datetime.now() - cached["timestamp"] < OPTION_CACHE_TTL:
            return cached["data"]
    return None

def set_cached_option_chain(symbol: str, expiration: str, option_chain: OptionChain):
    cache_key = (symbol, expiration)
    cache["option_chains"][cache_key] = {
        "data": option_chain,
        "timestamp": datetime.now()
    }

class OptionData(BaseModel):
    strike: float
    option_type: str
    open_interest: Optional[int]
    volume: Optional[int]
    delta: Optional[float]
    gamma: Optional[float]
    theta: Optional[float]

class MarketDataResponse(BaseModel):
    symbol: str
    price: float
    volume: int
    expiration: str
    calls: List[OptionData]
    puts: List[OptionData]
    put_call_volume_ratio: Optional[float]
    cached: bool
    timestamp: str

@app.get("/")
async def root():
    return {
        "status": "healthy",
        "message": "Stock Dashboard API is running"
    }

@app.get("/market-data/{symbol}", response_model=MarketDataResponse)
async def get_market_data(
    symbol: str,
    expiration: str = Query(..., description="Expiration date in YYYY-MM-DD format"),
    num_strikes: int = Query(10, ge=1, le=50, description="Number of strikes around current price")
):
    symbol = symbol.upper()
    was_cached = False

    cached_chain = get_cached_option_chain(symbol, expiration)

    if cached_chain:
        option_chain = cached_chain
        was_cached = True
    else:
        cached_ticker = get_cached_ticker(symbol)

        if cached_ticker:
            ticker = cached_ticker
        else:
            try:
                alpha_vantage_key = config("ALPHA_VANTAGE_API_KEY")
            except Exception:
                raise HTTPException(
                    status_code=500,
                    detail="ALPHA_VANTAGE_API_KEY not configured"
                )

            av = alphaVantage(alpha_vantage_key, symbol)
            ticker = av.get_stock_data()

            if ticker is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"Could not fetch ticker data for {symbol}"
                )

            set_cached_ticker(symbol, ticker)

        try:
            polygon_key = config("POLYGON_API_KEY")
        except Exception:
            raise HTTPException(
                status_code=500,
                detail="POLYGON_API_KEY not configured"
            )

        polygon = polygonAPI(polygon_key)
        option_chain = polygon.get_optionchain_data(ticker, expiration, num_strikes=num_strikes)

        if option_chain is None:
            raise HTTPException(
                status_code=404,
                detail=f"Could not fetch option chain for {symbol} with expiration {expiration}"
            )

        set_cached_option_chain(symbol, expiration, option_chain)

    calls = []
    puts = []

    for strike, option in option_chain.call_chain.items():
        calls.append(OptionData(
            strike=strike,
            option_type=option.option_type,
            open_interest=option.open_interest,
            volume=option.volume,
            delta=option.delta,
            gamma=option.gamma,
            theta=option.theta
        ))

    for strike, option in option_chain.put_chain.items():
        puts.append(OptionData(
            strike=strike,
            option_type=option.option_type,
            open_interest=option.open_interest,
            volume=option.volume,
            delta=option.delta,
            gamma=option.gamma,
            theta=option.theta
        ))

    analytics_obj = analytics(option_chain)
    pc_ratio = analytics_obj.put_call_volume_ratio(option_chain)
    ###need all analysis fetched here then inputted into MarketDataResponse for ease of access
    return MarketDataResponse(
        symbol=option_chain.ticker.symbol,
        price=float(option_chain.ticker.price),
        volume=int(option_chain.ticker.volume),
        expiration=option_chain.date,
        calls=sorted(calls, key=lambda x: x.strike),
        puts=sorted(puts, key=lambda x: x.strike),
        put_call_volume_ratio=pc_ratio,
        cached=was_cached,
        timestamp=datetime.now().isoformat()
    )

@app.get("/cache/status")
async def cache_status():
    return {
        "tickers_cached": len(cache["tickers"]),
        "option_chains_cached": len(cache["option_chains"]),
        "ticker_ttl_seconds": int(TICKER_CACHE_TTL.total_seconds()),
        "option_ttl_seconds": int(OPTION_CACHE_TTL.total_seconds())
    }

@app.post("/cache/clear")
async def clear_cache():
    cache["tickers"].clear()
    cache["option_chains"].clear()
    return {"message": "Cache cleared successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
