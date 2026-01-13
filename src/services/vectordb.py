import os
import random
from typing import List
# import asyncpg  # Uncomment when you have real DB

class VectorDB:
    """
    Abstraction for the pgvector database.
    """
    def __init__(self):
        self.db_url = os.getenv("DATABASE_URL", "postgresql://postgres:[YOUR_PASSWORD]@db.cqzcbfgnpyyiknfzybom.supabase.co:5432/postgres")
        self.mock_mode = True  # Set to False when you have a real DB running

    async def search(self, query: str, limit: int = 3) -> List[str]:
        """
        Simulate a vector search.
        In production, this embeds the query and SQL selects from pgvector.
        """
        if self.mock_mode:
            # MOCK DATA: Returns fake search results for testing logic
            print(f"  [DB Log] Searching knowledge base for: '{query}'")
            mock_knowledge = [
                "De Pauluskerk biedt dagopvang van 09:00 tot 16:00.",
                "Voor medische hulp kun je terecht bij de straatdokter op dinsdag.",
                "De politie kan helpen bij aangifte van ID-verlies, maar geeft geen opvang.",
                "Nachtopvang 'De Boeg' heeft plekken beschikbaar na 17:00."
            ]
            matches = [k for k in mock_knowledge if any(word in k.lower() for word in query.lower().split())]
            return matches if matches else [mock_knowledge[0]]  # Always return a list
        
        return []  