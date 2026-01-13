import asyncio
import json
import os
from typing import Any, Dict, List, Optional

import asyncpg
import psycopg2
from dotenv import load_dotenv
from openai import AsyncOpenAI

# --- 1. Load Environment Variables Once ---
load_dotenv()

# --- 2. Fetch Variables & Construct Connection String ---
# We try to get the variables (supporting both lowercase as in your code and uppercase standards)
DB_USER = os.getenv("user") or os.getenv("DB_USER")
DB_PASSWORD = os.getenv("password") or os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("host") or os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("port") or os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("dbname") or os.getenv("DB_NAME")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Construct DATABASE_URL if it's missing but we have the parts
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL and DB_USER and DB_PASSWORD and DB_HOST and DB_NAME:
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    # Inject it back into os.environ so other libs can find it if needed
    os.environ["DATABASE_URL"] = DATABASE_URL

# --- 3. Synchronous Connection Test (psycopg2) ---
try:
    # Only attempt if we have credentials
    if DB_USER and DB_NAME:
        connection = psycopg2.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME
        )
        print("✅ [Sync] Connection successful!")
        
        cursor = connection.cursor()
        cursor.execute("SELECT NOW();")
        result = cursor.fetchone()
        print(f"🕒 [Sync] Current Time: {result}")

        cursor.close()
        connection.close()
        print("🔒 [Sync] Connection closed.")
    else:
        print("⚠️ [Sync] Skipping sync test: Missing DB credentials in .env")

except Exception as e:
    print(f"❌ [Sync] Failed to connect: {e}")

# --- 4. Vector Database Class (Async) ---
class VectorDB:
    """
    Production-ready Vector Database abstraction for Supabase (pgvector).
    """

    def __init__(self):
        """
        Initializes the database connection string and OpenAI client.
        """
        self.db_url = os.getenv("DATABASE_URL")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")

        if not self.db_url:
            raise ValueError("CRITICAL: 'DATABASE_URL' is missing from environment variables.")
        if not self.openai_api_key:
            raise ValueError("CRITICAL: 'OPENAI_API_KEY' is missing from environment variables.")

        # Initialize Async OpenAI Client
        self.openai_client = AsyncOpenAI(api_key=self.openai_api_key)

    async def get_embedding(self, text: str) -> List[float]:
        """
        Generates a 1536-dimensional embedding using OpenAI's text-embedding-3-small.
        """
        try:
            response = await self.openai_client.embeddings.create(
                input=text.replace("\n", " "),
                model="text-embedding-3-small"
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"[Error] Failed to generate embedding: {e}")
            return []

    async def search(self, query: str, limit: int = 3, threshold: float = 0.7) -> List[Dict[str, Any]]:
        """
        Performs a semantic vector search on the 'knowledge_base' table.
        """
        # 1. Generate Embedding
        query_vector = await self.get_embedding(query)
        if not query_vector:
            return []

        conn = None
        try:
            # 2. Connect to Database directly
            conn = await asyncpg.connect(self.db_url)
            print("[Debug] Connected to DB successfully")

            # List public tables
            tables = await conn.fetch("SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename;")
            print("[Debug] Public tables:", ', '.join([row['tablename'] for row in tables]))

            # Check knowledge_base
            try:
                rlc = await conn.fetchval("SELECT relrowsecurity FROM pg_class WHERE relname = 'knowledge_base';")
                print(f"[Debug] knowledge_base RLS enabled: {rlc}")

                # Try simple select
                rows = await conn.fetch("SELECT id, content FROM knowledge_base LIMIT 1;")
                print(f"[Debug] Simple SELECT succeeded, sample rows count: {len(rows)}")
                if rows:
                    print(f"[Debug] Sample row: {dict(rows[0])}")
            except Exception as e2:
                print(f"[Debug] knowledge_base check failed: {e2}")

            # 3. Execute Vector Search SQL
            # We use the <=> operator for Cosine Distance.
            # (1 - distance) gives us the Similarity score.
            sql = """
                SELECT 
                    id, 
                    content, 
                    metadata, 
                    1 - (embedding <=> $1) as similarity
                FROM knowledge_base
                WHERE 1 - (embedding <=> $1) > $3
                ORDER BY embedding <=> $1
                LIMIT $2;
            """

            # asyncpg requires vectors to be passed as string representations for now
            rows = await conn.fetch(sql, str(query_vector), limit, threshold)

            # 4. Format the Results
            results = []
            for row in rows:
                # Handle metadata parsing
                meta = row['metadata']
                if isinstance(meta, str):
                    try:
                        meta = json.loads(meta)
                    except json.JSONDecodeError:
                        meta = {}

                results.append({
                    "id": row['id'],
                    "content": row['content'],
                    "metadata": meta,
                    "similarity": round(row['similarity'], 4)
                })

            return results

        except Exception as e:
            print(f"[Error] Database search failed: {e}")
            return []
        finally:
            if conn:
                await conn.close()

# --- 5. Test Block ---
if __name__ == "__main__":
    async def main():
        print("\n--- Initializing VectorDB ---")
        try:
            db = VectorDB()
            
            # Using your Dutch query example
            user_question = "Ik zoek een slaapplaats"
            print(f"🔎 Searching for: '{user_question}'...")
            
            results = await db.search(user_question, limit=2)
            
            if results:
                print(f"\n✅ Found {len(results)} matches:")
                for res in results:
                    print(f"\n[Score: {res['similarity']}]")
                    print(f"Content: {res['content'][:100]}...") 
                    print(f"Metadata: {res['metadata']}")
            else:
                print("\n⚠️ No results found. (Check if your DB is empty or threshold is too high)")

        except ValueError as e:
            print(f"Configuration Error: {e}")

    asyncio.run(main())
