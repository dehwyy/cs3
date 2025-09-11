import requests
from config import CRYPTOCURRENCIES

URL = "https://api.coingecko.com/api/v3/coins/markets"

def get_coin_data(symbol: str):
    coin = CRYPTOCURRENCIES.get(symbol.upper())
    if not coin:
        return None

    params = {
        "vs_currency": "usd",
        "ids": coin
    }
    resp = requests.get(URL, params=params)
    if resp.status_code != 200:
        return None

    data = resp.json()
    if not data:
        return None

    coin_data = data[0]
    return {
        "price": coin_data.get("current_price"),
        "change_24h": coin_data.get("price_change_percentage_24h"),
        "high_24h": coin_data.get("high_24h"),
        "low_24h": coin_data.get("low_24h"),
    }

def get_multiple(symbols):
    coins = [CRYPTOCURRENCIES.get(s.upper()) for s in symbols if CRYPTOCURRENCIES.get(s.upper())]
    if not coins:
        return []
    params = {
        "vs_currency": "usd",
        "ids": ",".join(coins)
    }
    resp = requests.get(URL, params=params)
    if resp.status_code != 200:
        return []
    return resp.json()
