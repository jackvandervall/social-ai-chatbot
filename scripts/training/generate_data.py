"""
Script for generating synthetic training data for the RotterMaatje chatbot.

This module handles the generation of both Supervised Fine-Tuning (SFT) 
and Direct Preference Optimization (DPO) datasets by combining real 
FAQ/APV data with synthetic conversations generated via an LLM.
"""

import json
import os
import random
import time
import sys
from pathlib import Path
from typing import List, Dict
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

# --- PATH CONFIGURATION ---
ROOT_DIR = Path(__file__).resolve().parents[3]
DATA_KNOWLEDGE_DIR = ROOT_DIR / "data" / "processed"
OUTPUT_DIR = ROOT_DIR / "Jack" / "data"

# Add project root to sys.path to import src modules
sys.path.append(str(ROOT_DIR))

try:
    from src.core.prompts import PromptConfig
    SYSTEM_PROMPT = PromptConfig.get_system_prompt()
except ImportError:
    # Fallback if import fails (e.g. structure issues), though sys.path should fix it
    print("Warning: Could not import PromptConfig. Using fallback prompt.")
    SYSTEM_PROMPT = """You are RotterMaatje, a helpful, empathetic assistant for volunteers helping the homeless in Rotterdam.
    Communicate in the user's language at B1 level. Be culturally sensitive.
    Prioritize safety and provide accurate information."""

# Load .env
load_dotenv(ROOT_DIR / ".env")

# --- LLM CONFIGURATION ---
provider = os.getenv("MODEL_PROVIDER", "openrouter").lower()
api_key = os.getenv("OPENROUTER_API_KEY") if provider == "openrouter" else os.getenv("OPENAI_API_KEY")
base_url = "https://openrouter.ai/api/v1" if provider == "openrouter" else os.getenv("OPENAI_BASE_URL")

# Use a confirmed OpenRouter model (DeepSeek V3 is very capable and cheap)
MODEL_NAME = "deepseek/deepseek-chat" 

client = OpenAI(
    base_url=base_url,
    api_key=api_key
)

LANGUAGES = [
    {"name": "Dutch", "code": "nl"},
    {"name": "English", "code": "en"},
    {"name": "Polish", "code": "pl"},
    {"name": "Arabic", "code": "ar"},
]

def load_unified_knowledge() -> List[Dict]:
    """
    Loads FAQ and APV data from the knowledge directory.
    """
    all_knowledge = []
    
    files = ["faq_structured.json", "apv_structured.json"]
    for filename in files:
        file_path = DATA_KNOWLEDGE_DIR / filename
        if file_path.exists():
            print(f"Loading knowledge from {filename}...")
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                all_knowledge.extend(data)
        else:
            print(f"Warning: {file_path} not found.")
            
    return all_knowledge

def generate_sft_data(knowledge_base: List[Dict], count=10):
    """
    Generates multi-turn conversations grounded in real knowledge.
    """
    print(f"Generating {count} synthetic SFT examples...")
    examples = []
    
    for i in range(count):
        item = random.choice(knowledge_base)
        lang = random.choice(LANGUAGES)
        
        prompt = f"""Generate a realistic chatbot conversation for 'RotterMaatje'.
        
        SYSTEM PERSONA (The 'assistant' MUST follow this):
        {SYSTEM_PROMPT}
        
        CONTEXT DATA (Raw facts - REPHRASE these to match the persona's tone):
        Question: {item['vraag']}
        Answer: {item['antwoord']}
        Category: {item.get('metadata', {}).get('categorie', 'General')}
        
        Target Language: {lang['name']}
        
        Instructions:
        1. Create a conversation where a user asks about the context topic in the Target Language.
        2. The assistant responds using the SYSTEM PERSONA.
        3. CRITICAL: Only respond to what the user actually said. DO NOT assume they just got out of prison, had a divorce, etc., unless they explicitly say so.
        4. STRICTLY AVOID copying the raw Answer if it is rude, bureaucratic, or harsh (e.g. APV legal text). Adapt it to be helpful and empathetic.
        5. Provide 2-3 turns.
        
        Format the output as a JSON object with a 'messages' key containing a list of roles (user/assistant) and 'content'.
        """
        
        try:
            print(f"  [{i+1}/{count}] Requesting SFT example for topic: {item['vraag'][:30]}...")
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            
            content = json.loads(response.choices[0].message.content)
            messages = content.get("messages", [])
            if messages:
                examples.append({"messages": messages})
                print(f"  Done.")
            time.sleep(1) # Simple rate limiting safeguard
        except Exception as e:
            print(f"Error generating SFT: {e}")
            
    return examples

def generate_dpo_from_knowledge(knowledge_base: List[Dict], count=15):
    """
    Generates DPO pairs using real knowledge as grounding for accuracy.
    """
    print(f"Generating {count} DPO examples from knowledge base...")
    examples = []
    
    if count > len(knowledge_base):
        sampled = random.choices(knowledge_base, k=count)
    else:
        sampled = random.sample(knowledge_base, count)
    
    for i, item in enumerate(sampled):
        lang = random.choice(LANGUAGES)
        
        prompt = f"""Generate a DPO (Direct Preference Optimization) triplet for 'RotterMaatje'.

        SYSTEM PERSONA (Defines the 'chosen' response style):
        {SYSTEM_PROMPT}

        KNOWLEDGE SOURCE (Raw Information):
        Question: {item['vraag']}
        Correct Answer: {item['antwoord']}

        Target Language: {lang['name']}
        
        Instructions:
        1. 'prompt': A realistic user question in {lang['name']}.
        2. 'chosen': The PERFECT response in {lang['name']}. It MUST:
           - Use the System Persona (empathetic, helpful, B1 level).
           - Only respond to the prompt's content. DO NOT assume or invent a backstory (e.g., being an ex-prisoner) if not mentioned.
           - Use the Knowledge Source facts but REPHRASE them to be kind.
        3. 'rejected': A BAD response. It should be:
           - Rude, dismissive, or overly bureaucratic.
           - Falsely assuming a backstory (e.g., assuming they are from prison when they didn't say so).
           - Factually incorrect or wrong language.
        
        Return a JSON object with keys: 'prompt', 'chosen', 'rejected'.
        """
        
        try:
            print(f"  [{i+1}/{count}] Requesting DPO triplet for topic: {item['vraag'][:30]}...")
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            
            content = json.loads(response.choices[0].message.content)
            if all(k in content for k in ["prompt", "chosen", "rejected"]):
                examples.append(content)
                print(f"  Done.")
            time.sleep(1)
        except Exception as e:
            print(f"Error generating DPO: {e}")
    
    return examples

if __name__ == "__main__":
    # Ensure output dir exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1. Load Knowledge
    kb = load_unified_knowledge()
    if not kb:
        print("No knowledge found. Exiting.")
        exit(1)
        
    print("Skipping raw data copy to prevent SFT pollution with harsh tone. Relying on synthetic rewrite.")
    
    # 3. Generate synthetic SFT (Multi-turn)
    synth_sft = generate_sft_data(kb, count=2)
    
    random.shuffle(synth_sft)
    
    sft_output_path = OUTPUT_DIR / "processed" / "synthetic_train.jsonl"
    sft_output_path.parent.mkdir(parents=True, exist_ok=True)
    # Append mode ("a") to add to existing data
    with open(sft_output_path, "a", encoding="utf-8") as f:
        for ex in synth_sft:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")
            
    combined_dpo = generate_dpo_from_knowledge(kb, count=0)
    
    dpo_output_path = OUTPUT_DIR / "processed" / "synthetic_dpo.jsonl"
    # Append mode ("a") to add to existing data
    with open(dpo_output_path, "a", encoding="utf-8") as f:
        for ex in combined_dpo:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")
            
    print(f"\nFINISH STATUS:")
    print(f"- NEW SFT examples added: {len(synth_sft)}")
    print(f"- NEW DPO examples added: {len(combined_dpo)}")
    print(f"- Files appended in: {OUTPUT_DIR / 'processed'}")

