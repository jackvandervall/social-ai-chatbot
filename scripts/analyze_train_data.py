
import json
import re
from collections import Counter
from pathlib import Path

# Paths
sft_path = Path("Jack/data/processed/synthetic_train.jsonl")
dpo_path = Path("Jack/data/processed/synthetic_dpo.jsonl")

def analyze_file(path, file_type="SFT"):
    if not path.exists():
        print(f"File not found: {path}")
        return

    print(f"--- Analyzing {file_type} ({path.name}) ---")
    
    data = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                try:
                    data.append(json.loads(line))
                except json.JSONDecodeError:
                    pass

    print(f"Total rows: {len(data)}")

    # Language Heuristics (Simple)
    langs = Counter()
    topics = Counter()
    prison_mentions = 0
    hallucination_check = 0

    keywords = {
        "Sleep/Shelter": ["slapen", "sleep", "mÃ³j", "nocleg", "mÃ¡wy", "opvang", "shelter", "bed", "dakloos", "homeless"],
        "Food": ["eten", "food", "honger", "hungry", "brood", "bread", "soep", "soup"],
        "Money/Income": ["geld", "money", "uitkering", "bijstand", "income"],
        "Hygiene/Clothes": ["douche", "shower", "kleding", "clothes", "wassen", "wash"],
        "Medical": ["arts", "doctor", "ziek", "sick", "pijn", "pain", "medicijnen"],
        "Legal/ID": ["bsn", "paspoort", "id", "postadres", "briefadres", "address"],
        "Drugs/Addiction": ["drugs", "verslaving", "addiction", "alcohol", "bier", "beer"],
        "Return Home": ["terug", "return", "land", "country", "barka"],
        "Nuisance/Police": ["politie", "police", "overlast", "nuisance", "boete", "fine", "mosquito"],
    }

    for item in data:
        text_content = ""
        if file_type == "SFT":
            # Check user messages
            for msg in item.get("messages", []):
                text_content += msg.get("content", "") + " "
        else: # DPO
            text_content += item.get("prompt", "") + " "
            text_content += item.get("chosen", "") + " "
        
        text_lower = text_content.lower()

        # Language detection (very rough)
        if re.search(r'[a-zA-ZÀ-ÿ]', text_lower) and not re.search(r'[\u0600-\u06FF]', text_lower): # Latin script
            if " the " in text_lower or " and " in text_lower:
                langs["English"] += 1
            elif " het " in text_lower or " de " in text_lower or " ik " in text_lower:
                langs["Dutch"] += 1
            elif " w " in text_lower or " z " in text_lower or "czy" in text_lower:
                langs["Polish"] += 1
            else:
                langs["Latin-Other"] += 1
        elif re.search(r'[ا-ي]', text_lower): # Arabic script
            langs["Arabic"] += 1

        # Topic detection
        matched_topic = False
        for topic, words in keywords.items():
            if any(w in text_lower for w in words):
                topics[topic] += 1
                matched_topic = True
        
        if not matched_topic:
            topics["Other/Unknown"] += 1

        # Check specific anti-hallucination/prison mentions
        if "gevangenis" in text_lower or "prison" in text_lower or "sjin" in text_lower or "jail" in text_lower:
            prison_mentions += 1

    print("\nLanguage Distribution (Approx):")
    for l, c in langs.most_common():
        print(f"  {l}: {c} ({c/len(data)*100:.1f}%)")

    print("\nTopic Distribution:")
    for t, c in topics.most_common():
        print(f"  {t}: {c} ({c/len(data)*100:.1f}%)")

    print(f"\nPrison/Jail Context Frequency: {prison_mentions} occurrences ({prison_mentions/len(data)*100:.1f}%)")
    print("-" * 40)

analyze_file(sft_path, "SFT")
analyze_file(dpo_path, "DPO")
