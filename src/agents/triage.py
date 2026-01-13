from pydantic import BaseModel, Field
from typing import Optional
from core.llm import get_model
from core.prompts import PromptConfig
from pydantic_ai import Agent

class TriageStatus(BaseModel):
    """
    Structured triage classification for user input.
    """
    topic: str = Field(
        ...,
        description="Primary topic: one of 'shelter', 'medical', 'food', 'legal', 'social', 'other'"
    )
    language: str = Field(
        ...,
        description="Detected primary language: 'nl', 'en', 'pl', 'ar'"
    )
    is_emergency: bool = Field(
        False,       
        description="True ONLY for immediate life-threatening situations (e.g., active bleeding, chest pain, suicide ATTEMPT). False for ideation/discussion."
    )
    reasoning: str = Field(
        ...,
        description="Brief explanation of classification (1-2 sentences)."
    )
    disclaimer_type: str = Field(
        'none',
        description="Disclaimer level: 'none', 'info' (general), 'caution' (sensitive e.g. drugs/suicide ideation), 'urgent' (high risk but not immediate)"
    )

# Triage agent for classification
triage_agent = Agent(
    model=get_model(),
    output_type=TriageStatus,
    system_prompt=PromptConfig.get_triage_prompt(),
)