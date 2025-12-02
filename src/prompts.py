# ============================================================================
# prompts.py - Centralized prompt management
# ============================================================================

from pathlib import Path
from typing import Dict

class PromptConfig:
    """Manages system prompts and guardrails for the Rotterdam agent."""
    
    # Defining prompts
    SYSTEM_PROMPT = """
Your name is RotterMaatje are a helpful, empathetic assistant for volunteers helping the homeless in Rotterdam.

Your primary goals:
- Provide accurate information about local services
- Detect emergencies and guide users to immediate help
- Communicate in the user's language (Dutch, English, Polish, Arabic)
- Be culturally sensitive and trauma-informed

Response guidelines:
- Keep responses clear and actionable
- Always prioritize safety
- Provide specific addresses and contact information when available
- If uncertain, acknowledge it and suggest alternatives
"""
    GUARDRAILS = {
        "emergency_keywords": [
            "bleeding", "bloeden", "krwawienie", "نزيف",
            "suicide", "zelfmoord", "samobójstwo", "انتحار",
            "violence", "geweld", "przemoc", "عنف",
            "chest pain", "pijn op de borst", "ból w klatce piersiowej", "ألم في الصدر"
        ],
        "max_response_length": None, # No max response length set
    }

    SAFETY_DISCLAIMERS = {
        "emergency": "⚠️ Als dit een noodgeval is, bel 112 onmiddellijk. | If this is an emergency, call 112 immediately.",
        "medical": "ℹ️ Dit is geen medisch advies. Raadpleeg een arts voor diagnose. | This is not medical advice.",
        "legal": "ℹ️ Dit is geen juridisch advies. Zoek een advocaat voor uw specifieke situatie. | This is not legal advice."
    }

    @classmethod
    def get_system_prompt(cls) -> str:
        """Returns the main system prompt."""
        return cls.SYSTEM_PROMPT.strip()
    
    @classmethod
    def check_emergency_keywords(cls, text: str) -> bool:
        """Check if text contains emergency keywords."""
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in cls.GUARDRAILS["emergency_keywords"])
