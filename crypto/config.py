import os

API_TOKEN = os.getenv("API_TOKEN", "8411407448:AAHbCv8VPnwNP-2TZjklzUnuodHU4As_qY0")

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

CRYPTOCURRENCIES = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "TRX": "tron",
    "SOL": "solana",
    "USDT": "tether",
}
