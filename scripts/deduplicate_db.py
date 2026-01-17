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

async def deduplicate():
    url = get_db_url()
    conn = await asyncpg.connect(url, statement_cache_size=0)
    try:
        print("Deduplicating 'knowledge_base' based on 'content'...")
        # Keep the row with the smallest ID for each unique content
        await conn.execute("""
            DELETE FROM knowledge_base
            WHERE id IN (
                SELECT id
                FROM (
                    SELECT id, ROW_NUMBER() OVER (PARTITION BY content ORDER BY id) as row_num
                    FROM knowledge_base
                ) t
                WHERE t.row_num > 1
            );
        """)
        print("Deduplication complete.")
        
        print("Now adding unique constraint...")
        await conn.execute("ALTER TABLE knowledge_base ADD CONSTRAINT unique_content UNIQUE (content);")
        print("Unique constraint added successfully.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(deduplicate())
