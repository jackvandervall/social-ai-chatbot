import asyncio
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project root to sys.path
project_root = Path(__file__).resolve().parents[1]
sys.path.append(str(project_root))

from src.services.pgvectordb import VectorDB

load_dotenv()

async def test_search():
    db = VectorDB()
    query = "Mag ik bedelen in Rotterdam?"
    print(f"Searching for: '{query}'")
    results = await db.search(query, limit=2)
    
    for i, res in enumerate(results):
        print(f"\nResult {i+1} (Similarity: {res['similarity']}):")
        print(f"Content: {res['content']}")
        print(f"Source: {res['source_url']} ({res['source_type']})")

if __name__ == "__main__":
    asyncio.run(test_search())
