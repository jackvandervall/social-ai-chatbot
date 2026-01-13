"""
Script for generating synthetic training data for the RotterMaatje chatbot.

This module handles the generation of both Supervised Fine-Tuning (SFT) 
and Direct Preference Optimization (DPO) datasets by combining real 
FAQ data with synthetic conversations generated via an LLM.
"""

import json
import os
import random
from typing import List, Dict
from openai import OpenAI
from pydantic import BaseModel

# Initialize Client (Assumes OPENROUTER_API_KEY or OPENAI_API_KEY in environment)
client = OpenAI(
    base_url=os.getenv("OPENAI_BASE_URL", "https://openrouter.ai/api/v1"),
    api_key=os.getenv("OPENROUTER_API_KEY", os.getenv("OPENAI_API_KEY"))
)

TOPICS = [
    {"topic": "Emergency Shelter", "facts": "Nachtopvang is available at Pauluskerk (Schiekade 3) and Centraal Onthaal. Emergency contact: 112."},
    {"topic": "Medical Care", "facts": "Street doctor (Straatdokter) is available on Tuesdays at Pauluskerk. Basic first aid provided by volunteers."},
    {"topic": "Food & Meals", "facts": "Free soup and bread served daily at 12:00 at Pauluskerk. No ID required for first-time visitors."},
    {"topic": "Legal Aid", "facts": "Legal advice (Rechtshulp) for undocumented people is available on Thursdays at the church office."},
]

LANGUAGES = [
    {"name": "Dutch", "code": "nl"},
    {"name": "English", "code": "en"},
    {"name": "Polish", "code": "pl"},
    {"name": "Arabic", "code": "ar"},
]

class SFTExample(BaseModel):
    messages: List[Dict[str, str]]

class DPOExample(BaseModel):
    prompt: str
    chosen: str
    rejected: str

def generate_sft_data(count=5):
    """
    Generates multi-turn conversations for Supervised Fine-Tuning (SFT).

    Args:
        count (int): The number of synthetic conversations to generate.
    """
    print(f"Generating {count} SFT examples...")
    examples = []
    
    for _ in range(count):
        topic = random.choice(TOPICS)
        lang = random.choice(LANGUAGES)
        
        prompt = f"""Generate a realistic chatbot conversation for a social service bot called 'RotterMaatje'.
        The bot helps homeless people in Rotterdam.
        
        Language: {lang['name']}
        Topic: {topic['topic']}
        Key Facts to include: {topic['facts']}
        
        Format the output as a JSON list of messages with 'role' (user/assistant) and 'content'.
        Provide 2-3 turns (user-assistant-user-assistant).
        The bot should be helpful, empathetic, and professional.
        """
        
        response = client.chat.completions.create(
            model="deepseek/deepseek-v3.2",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        content = json.loads(response.choices[0].message.content)
        # Handle different potential JSON keys from LLM
        messages = content.get("messages", content.get("conversation", []))
        if messages:
            examples.append({"messages": messages})
            
    with open("Jack/data/synthetic_train.jsonl", "w", encoding="utf-8") as f:
        for ex in examples:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")
    print("SFT data saved to Jack/data/synthetic_train.jsonl")

def generate_dpo_data(count=5):
    """
    Generates preference pairs for Reinforcement Learning (DPO).

    Args:
        count (int): The number of synthetic DPO triplets to generate.
    """
    print(f"Generating {count} DPO examples...")
    examples = []
    
    for _ in range(count):
        topic = random.choice(TOPICS)
        lang = random.choice(LANGUAGES)
        
        prompt = f"""Generate a DPO (Direct Preference Optimization) triplet for the 'RotterMaatje' bot.
        
        Language: {lang['name']}
        Topic: {topic['topic']}
        Fact: {topic['facts']}
        
        Return a JSON object with:
        - 'prompt': A user question in {lang['name']}.
        - 'chosen': A perfect, empathetic, factually correct answer in {lang['name']}.
        - 'rejected': A bad answer (e.g., wrong language, hallucinated location, rude tone, or forgetting the church address).
        """
        
        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        examples.append(json.loads(response.choices[0].message.content))
            
    with open("Jack/data/synthetic_dpo.jsonl", "w", encoding="utf-8") as f:
        for ex in examples:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")
    print("DPO data saved to Jack/data/synthetic_dpo.jsonl")

def load_real_faq_data():
    """
    Loads real FAQ data from JSON and converts it to SFT format.

    Returns:
        list[dict]: A list of conversation dictionaries formatted for SFT.
    """
    print("Loading real FAQ data...")
    examples = []
    
    faq_path = "Jack/data/faq_structured.json"
    if not os.path.exists(faq_path):
        print(f"Warning: {faq_path} not found. Skipping real data.")
        return examples
    
    with open(faq_path, "r", encoding="utf-8") as f:
        faq_data = json.load(f)
    
    for item in faq_data:
        # Convert Dutch FAQ to chat format
        messages = [
            {"role": "user", "content": item["vraag"]},
            {"role": "assistant", "content": item["antwoord"]}
        ]
        examples.append({"messages": messages})
    
    print(f"Loaded {len(examples)} real FAQ examples.")
    return examples


def generate_dpo_from_faq(count=10):
    """
    Generates DPO pairs using real FAQ data as grounding for accuracy.

    Args:
        count (int): The number of DPO triplets to generate from FAQ items.

    Returns:
        list[dict]: A list of DPO triplets (prompt, chosen, rejected).
    """
    print(f"Generating {count} DPO examples from real FAQ...")
    examples = []
    
    faq_path = "Jack/data/faq_structured.json"
    if not os.path.exists(faq_path):
        print(f"Warning: {faq_path} not found. Using generic topics instead.")
        return []
    
    with open(faq_path, "r", encoding="utf-8") as f:
        faq_data = json.load(f)
    
    # Sample FAQ items for DPO
    sampled = random.sample(faq_data, min(count, len(faq_data)))
    
    for item in sampled:
        lang = random.choice(LANGUAGES)
        
        prompt = f"""Generate a DPO triplet for training a social service chatbot.

        REAL FAQ (Dutch):
        Question: {item['vraag']}
        Correct Answer: {item['antwoord']}
        Category: {item['metadata']['categorie']}

        Target Language: {lang['name']}
        
        Return a JSON object with:
        - 'prompt': The user question translated to {lang['name']}.
        - 'chosen': The correct answer translated to {lang['name']}, maintaining all specific addresses and details.
        - 'rejected': A BAD answer that makes one of these mistakes:
          1. Wrong address (e.g., swapping Pauluskerk for NAS location)
          2. Wrong language (e.g., replying in Dutch when asked in Polish)
          3. Rude or dismissive tone
          4. Hallucinated information not in the original answer
        """
        
        response = client.chat.completions.create(
            model="deepseek/deepseek-v3.2",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        examples.append(json.loads(response.choices[0].message.content))
    
    return examples


if __name__ == "__main__":
    # Ensure data dir exists
    os.makedirs("Jack/data", exist_ok=True)
    
    # 1. Load real FAQ data
    real_data = load_real_faq_data()
    
    # 2. Generate synthetic SFT data
    generate_sft_data(count=10)
    
    # 3. Merge real + synthetic into final training file
    with open("Jack/data/synthetic_train.jsonl", "r", encoding="utf-8") as f:
        synthetic_data = [json.loads(line) for line in f]
    
    combined_data = real_data + synthetic_data
    random.shuffle(combined_data)
    
    with open("Jack/data/synthetic_train.jsonl", "w", encoding="utf-8") as f:
        for ex in combined_data:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")
    print(f"Combined {len(combined_data)} examples (real + synthetic) saved.")
    
    # 4. Generate DPO data from real FAQ (better grounding)
    dpo_from_faq = generate_dpo_from_faq(count=15)
    
    # 5. Also generate some purely synthetic DPO
    generate_dpo_data(count=5)
    
    # 6. Merge DPO data
    with open("Jack/data/synthetic_dpo.jsonl", "r", encoding="utf-8") as f:
        synthetic_dpo = [json.loads(line) for line in f]
    
    combined_dpo = dpo_from_faq + synthetic_dpo
    random.shuffle(combined_dpo)
    
    with open("Jack/data/synthetic_dpo.jsonl", "w", encoding="utf-8") as f:
        for ex in combined_dpo:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")
    print(f"Combined {len(combined_dpo)} DPO examples saved.")
