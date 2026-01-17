"""
Generic Knowledge Base Ingestion Script

This script ingests structured JSON files into the knowledge_base table.
It automatically detects the structure and can handle both APV and FAQ data.

Usage:
    python ingest_knowledge.py                    # Ingest all JSON files in data folder
    python ingest_knowledge.py apv                # Ingest only APV data
    python ingest_knowledge.py faq                # Ingest only FAQ data
    python ingest_knowledge.py path/to/file.json  # Ingest a specific file
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Optional

# Add project root to sys.path
project_root = Path(__file__).resolve().parents[1]
sys.path.append(str(project_root))

from src.services.pgvectordb import VectorDB


# Default data directory
DATA_DIR = project_root / "data" / "knowledge"

# Known source types and their URLs
SOURCE_CONFIG = {
    "apv": {
        "source_type": "apv",
        "source_url": "https://www.rotterdam.nl/openbare-orde",
        "bron": "APV Rotterdam"
    },
    "faq": {
        "source_type": "faq",
        "source_url": "https://www.pauluskerk.nl",
        "bron": "Pauluskerk FAQ"
    }
}


def detect_source_type(file_path: Path) -> str:
    """Detect source type based on filename."""
    filename = file_path.stem.lower()
    if "apv" in filename:
        return "apv"
    elif "faq" in filename:
        return "faq"
    else:
        # Default to generic if unknown
        return "generic"


def get_source_config(source_type: str) -> dict:
    """Get source configuration for a given type."""
    return SOURCE_CONFIG.get(source_type, {
        "source_type": source_type,
        "source_url": "",
        "bron": source_type.upper()
    })


def transform_item(item: dict, source_config: dict) -> dict:
    """
    Transform a structured JSON item into the format expected by VectorDB.
    
    Supports the standard format:
    {
        "vraag": "...",
        "antwoord": "...",
        "metadata": {
            "categorie": "...",
            "doelgroep": "...",
            "trefwoorden": [...]
        }
    }
    """
    # Build content from vraag/antwoord
    content_parts = []
    if "vraag" in item:
        content_parts.append(f"Vraag: {item['vraag']}")
    if "antwoord" in item:
        content_parts.append(f"Antwoord: {item['antwoord']}")
    
    # If no vraag/antwoord, try to use 'content' or 'text' fields
    if not content_parts:
        if "content" in item:
            content_parts.append(item["content"])
        elif "text" in item:
            content_parts.append(item["text"])
    
    content = "\n".join(content_parts)
    
    # Build metadata
    metadata = {}
    item_metadata = item.get("metadata", {})
    
    if "categorie" in item_metadata:
        metadata["categorie"] = item_metadata["categorie"]
    if "doelgroep" in item_metadata:
        metadata["doelgroep"] = item_metadata["doelgroep"]
    if "trefwoorden" in item_metadata:
        trefwoorden = item_metadata["trefwoorden"]
        if isinstance(trefwoorden, list):
            metadata["trefwoorden"] = ", ".join(trefwoorden)
        else:
            metadata["trefwoorden"] = str(trefwoorden)
    
    # Add original question for reference
    if "vraag" in item:
        metadata["bron_vraag"] = item["vraag"]
    
    return {
        "content": content,
        "metadata": metadata,
        "source_type": source_config["source_type"],
        "source_url": source_config["source_url"],
        "bron": source_config["bron"]
    }


async def ingest_file(file_path: Path, source_type: Optional[str] = None) -> int:
    """
    Ingest a single JSON file into the knowledge base.
    
    Args:
        file_path: Path to the JSON file
        source_type: Override source type (auto-detected if not provided)
        
    Returns:
        Number of items ingested
    """
    if not file_path.exists():
        print(f"[Error] File not found: {file_path}")
        return 0
    
    # Auto-detect source type if not provided
    if source_type is None:
        source_type = detect_source_type(file_path)
    
    source_config = get_source_config(source_type)
    
    print(f"\n{'='*60}")
    print(f"Ingesting: {file_path.name}")
    print(f"Source Type: {source_config['source_type']}")
    print(f"Source URL: {source_config['source_url']}")
    print(f"Bron: {source_config['bron']}")
    print(f"{'='*60}")
    
    # Load JSON data
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Handle both list and dict formats
    if isinstance(data, dict):
        # If dict has an 'items' or 'data' key, use that
        if "items" in data:
            data = data["items"]
        elif "data" in data:
            data = data["data"]
        else:
            # Treat single dict as a list with one item
            data = [data]
    
    print(f"Loaded {len(data)} entries from {file_path.name}")
    
    # Transform items
    transformed_items = []
    for i, item in enumerate(data):
        try:
            transformed = transform_item(item, source_config)
            if transformed["content"]:  # Only add if content is not empty
                transformed_items.append(transformed)
            else:
                print(f"  [Warning] Skipping item {i+1}: No content found")
        except Exception as e:
            print(f"  [Error] Failed to transform item {i+1}: {e}")
    
    print(f"Transformed {len(transformed_items)} items for ingestion")
    
    if not transformed_items:
        print("[Warning] No items to ingest!")
        return 0
    
    # Ingest into database
    db = VectorDB()
    await db.upsert_batch(transformed_items)
    
    print(f"[Success] Ingested {len(transformed_items)} items from {file_path.name}")
    return len(transformed_items)


async def ingest_all(data_dir: Path = DATA_DIR) -> int:
    """
    Ingest all *_structured.json files from the data directory.
    
    Returns:
        Total number of items ingested
    """
    json_files = list(data_dir.glob("*_structured.json"))
    
    if not json_files:
        print(f"[Warning] No *_structured.json files found in {data_dir}")
        return 0
    
    print(f"Found {len(json_files)} structured JSON files to ingest:")
    for f in json_files:
        print(f"  - {f.name}")
    
    total = 0
    for file_path in json_files:
        count = await ingest_file(file_path)
        total += count
    
    print(f"\n{'='*60}")
    print(f"TOTAL: Ingested {total} items from {len(json_files)} files")
    print(f"{'='*60}")
    
    return total


async def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        # No arguments: ingest all files
        await ingest_all()
    else:
        arg = sys.argv[1].lower()
        
        if arg in ("apv", "faq"):
            # Ingest specific type
            file_name = f"{arg}_structured.json"
            file_path = DATA_DIR / file_name
            await ingest_file(file_path, source_type=arg)
        elif arg in ("-h", "--help", "help"):
            print(__doc__)
        else:
            # Treat as file path
            file_path = Path(arg)
            if not file_path.is_absolute():
                file_path = Path.cwd() / arg
            await ingest_file(file_path)


if __name__ == "__main__":
    asyncio.run(main())
