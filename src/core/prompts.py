# ============================================================================
# prompts.py - Centralized prompt management
# ============================================================================

from pathlib import Path
from typing import Dict

class PromptConfig:
    """Manages system prompts and guardrails for the Rotterdam agent."""
    
    # Main system prompt for RotterMaatje
    SYSTEM_PROMPT = """
You are RotterMaatje, a helpful, empathetic assistant for volunteers helping the homeless in Rotterdam.

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

IMPORTANT:
- You are a CHATBOT.
- DO NOT use the 'final_result' tool to return your answer. Just write the text.
"""
    
    # Triage system prompt for classification
    TRIAGE_PROMPT = """
You are a triage classifier for RotterMaatje, an AI assistant for Rotterdam homeless aid volunteers.

Classify the user input STRICTLY into TriageStatus JSON:

- topic: EXACTLY one of: 'shelter', 'medical', 'food', 'legal', 'social', 'other'
- language: Primary detected: 'nl' (Dutch), 'en' (English), 'pl' (Polish), 'ar' (Arabic)
- is_emergency: true ONLY for IMMEDIATE life-threat (active bleeding, chest pain NOW, suicide ATTEMPT in progress). False for discussion/ideation/planning.
- reasoning: 1-2 sentences explaining choices.
- disclaimer_type: 'none' (normal), 'info' (medical/legal general), 'caution' (sensitive: drugs/suicide ideation/abuse), 'urgent' (high risk, imminent harm but not immediate death)

Context: Rotterdam homeless services (Pauluskerk, shelters, Straatdokter, Leger des Heils). Be context-aware: "suicide thoughts" = caution (not emergency), "bleeding badly now" = emergency.

User message: {input}
Respond ONLY with valid TriageStatus JSON.
"""
    
    # Disclaimer messages by type
    DISCLAIMERS = {
        "none": "",
        "info": "\n\nℹ️ Dit is geen professioneel advies. Neem contact op met experts.",
        "caution": "\n\n⚠️ Gevoelig onderwerp. Voor drugs/hulp: Jellinek (010-4618888). Praat erover.",
        "urgent": "\n\n🚨 Urgent: Bel direct hulpdiensten als gevaar dreigt. 112 voor noodgevallen.",
        "emergency": "🚨 NOODGEVAL: Bel 112 onmiddellijk! | Call 112 now! Deze bot vervangt geen professionele hulp."
    }
    
    # Legacy guardrails (to be deprecated)
    GUARDRAILS = {
        "max_response_length": None,
    }
    
    @classmethod
    def get_system_prompt(cls) -> str:
        """Returns the main system prompt."""
        return cls.SYSTEM_PROMPT.strip()
    
    @classmethod
    def get_triage_prompt(cls) -> str:
        """Returns the triage classification prompt."""
        return cls.TRIAGE_PROMPT.strip()
    
    @classmethod
    def get_disclaimer(cls, disclaimer_type: str) -> str:
        """Get disclaimer text by type."""
        return cls.DISCLAIMERS.get(disclaimer_type, "")
    
    @classmethod
    def is_emergency_disclaimer(cls, is_emergency: bool) -> str:
        """Get emergency disclaimer if true."""
        if is_emergency:
            return cls.DISCLAIMERS["emergency"]
        return ""
