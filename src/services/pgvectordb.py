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
DB_USER = os.getenv("user") or os.getenv("DB_USER")
DB_PASSWORD = os.getenv("password") or os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("host") or os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("port") or os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("dbname") or os.getenv("DB_NAME")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL and DB_USER and DB_PASSWORD and DB_HOST and DB_NAME:
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# --- 4. Vector Database Class (Async) ---
class VectorDB:
    """
    Production-ready Vector Database abstraction for Supabase (pgvector).
    """

    def __init__(self):
        """
        Initializes the database connection string and OpenAI client.
        """
        self.db_url = DATABASE_URL
        self.openai_api_key = os.getenv("OPENAI_API_KEY")

        if not self.db_url:
            raise ValueError("CRITICAL: 'DATABASE_URL' is missing from environment variables.")
        if not self.openai_api_key:
            raise ValueError("CRITICAL: 'OPENAI_API_KEY' is missing from environment variables.")

        # Initialize Async OpenAI Client - force official URL for embeddings
        self.openai_client = AsyncOpenAI(
            api_key=self.openai_api_key,
            base_url="https://api.openai.com/v1"
        )

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

    async def search(self, query: str, limit: int = 3, threshold: float = 0.5) -> List[Dict[str, Any]]:
        """
        Performs a semantic vector search on the 'knowledge_base' table.
        """
        query_vector = await self.get_embedding(query)
        if not query_vector:
            return []

        conn = None
        try:
            # Set statement_cache_size=0 to work with Supabase Transaction Pooler (PgBouncer)
            conn = await asyncpg.connect(self.db_url, statement_cache_size=0)

            sql = """
                SELECT 
                    id, 
                    content, 
                    metadata, 
                    source_url,
                    source_type,
                    1 - (embedding <=> $1) as similarity
                FROM knowledge_base
                WHERE 1 - (embedding <=> $1) > $3
                ORDER BY embedding <=> $1
                LIMIT $2;
            """
            rows = await conn.fetch(sql, str(query_vector), limit, threshold)

            results = []
            for row in rows:
                meta = row['metadata']
                if isinstance(meta, str):
                    try: meta = json.loads(meta)
                    except: meta = {}
                results.append({
                    "id": row['id'],
                    "content": row['content'],
                    "metadata": meta,
                    "source_url": row['source_url'],
                    "source_type": row['source_type'],
                    "similarity": round(row['similarity'], 4)
                })
            return results
        except Exception as e:
            print(f"[Error] Database search failed: {e}")
            return []
        finally:
            if conn: await conn.close()
