import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_url():
    user = os.getenv("user")
    password = os.getenv("password")
    host = os.getenv("host")
    port = os.getenv("port", "5432")
    dbname = os.getenv("dbname")
    url = os.getenv("DATABASE_URL")
    if not url and user and password and host and dbname:
        url = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
    return url

DB_URL = get_db_url()

async def check_schema():
    conn = await asyncpg.connect(DB_URL, statement_cache_size=0)
    try:
        # Check constraints on knowledge_base
        constraints = await conn.fetch("""
            SELECT conname, pg_get_constraintdef(c.oid)
            FROM pg_constraint c
            JOIN pg_class t ON c.conrelid = t.oid
            WHERE t.relname = 'knowledge_base';
        """)
        print("Constraints on 'knowledge_base':")
        for con in constraints:
            print(f" - {con[0]}: {con[1]}")
            
        # Check indices
        indices = await conn.fetch("""
            SELECT indexname, indexdef
            FROM pg_indexes
            WHERE tablename = 'knowledge_base';
        """)
        print("\nIndices on 'knowledge_base':")
        for idx in indices:
            print(f" - {idx[0]}: {idx[1]}")
            
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(check_schema())
