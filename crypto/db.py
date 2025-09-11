import asyncpg
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS

async def get_db():
    return await asyncpg.connect(
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        host=DB_HOST,
        port=DB_PORT
    )

async def init_db():
    conn = await get_db()
    await conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        chat_id BIGINT UNIQUE,
        language TEXT DEFAULT 'ru'
    );
    CREATE TABLE IF NOT EXISTS favorites (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
        symbol TEXT
    );
    """)
    await conn.close()

# --- SQL запросы ---

async def get_user(chat_id: int):
    conn = await get_db()
    row = await conn.fetchrow("SELECT * FROM users WHERE chat_id=$1", chat_id)
    await conn.close()
    return row

async def add_user(chat_id: int, lang: str):
    conn = await get_db()
    await conn.execute(
        "INSERT INTO users (chat_id, language) VALUES ($1, $2) ON CONFLICT (chat_id) DO NOTHING",
        chat_id, lang
    )
    await conn.close()

async def update_language(chat_id: int, lang: str):
    conn = await get_db()
    await conn.execute("UPDATE users SET language=$1 WHERE chat_id=$2", lang, chat_id)
    await conn.close()

async def get_favorites(chat_id: int):
    conn = await get_db()
    rows = await conn.fetch(
        "SELECT symbol FROM favorites f JOIN users u ON u.id=f.user_id WHERE u.chat_id=$1",
        chat_id
    )
    await conn.close()
    return [r["symbol"] for r in rows]

async def add_favorite(chat_id: int, symbol: str):
    conn = await get_db()
    await conn.execute(
        "INSERT INTO favorites (user_id, symbol) VALUES ((SELECT id FROM users WHERE chat_id=$1), $2)",
        chat_id, symbol.upper()
    )
    await conn.close()

async def remove_favorite(chat_id: int, symbol: str):
    conn = await get_db()
    await conn.execute(
        "DELETE FROM favorites WHERE user_id=(SELECT id FROM users WHERE chat_id=$1) AND symbol=$2",
        chat_id, symbol.upper()
    )
    await conn.close()
