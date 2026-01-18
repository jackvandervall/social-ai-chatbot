import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ConfigDict
from pydantic_ai import Agent, RunContext
from typing import Optional
from agents.triage import TriageStatus
from pydantic_ai.models.openai import OpenAIChatModel
from services.pgvectordb import VectorDB
from core.prompts import PromptConfig
import chainlit as cl
from core.llm import get_model

# Load environment variables
load_dotenv()

# MODEL CONFIGURATION
MODEL_PROVIDER = os.getenv('MODEL_PROVIDER', 'openrouter')  # 'openrouter' or 'local'

# DEFINE DEPENDENCIES
class AgentDeps(BaseModel):
    """
    Defines the dependencies required by the agent during execution.
    
    Attributes:
        db (VectorDB): The vector database instance for RAG operations.
        triage_data (TriageStatus): Classification data from the triage agent.
        context_mode (str): Either 'volunteer' or 'direct' for homeless person mode.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)
    db: VectorDB
    triage_data: Optional[TriageStatus] = None
    context_mode: str = "volunteer"  # 'volunteer' or 'direct'

# DEFINE THE AGENT
rottermaatje_agent = Agent(
    model=get_model(),
    deps_type=AgentDeps,
)

# Dynamic system prompt based on context mode
@rottermaatje_agent.system_prompt
async def get_dynamic_system_prompt(ctx: RunContext[AgentDeps]) -> str:
    """Returns the appropriate system prompt based on context mode."""
    return PromptConfig.get_system_prompt(ctx.deps.context_mode)

# RAG tool
@rottermaatje_agent.tool
async def search_knowledge_base(ctx: RunContext[AgentDeps], query: str) -> str:
    """
    Search the internal database for specific information.
    
    This tool queries the vector database for details regarding shelters,
    medical help, or procedures. It should be used for factual user requests.
    
    Args:
        ctx (RunContext[AgentDeps]): The context containing agent dependencies.
        query (str): The search term or question to query the database with.
    
    Returns:
        str: A formatted string of search results or a default message if none found.
    """
    async with cl.Step(name="Interne kennisbank", type="tool"):
        results = await ctx.deps.db.search(query)
        if not results:
            return "Geen specifieke informatie gevonden in de database."
        contents = [r["content"] for r in results]
        return "- " + "\n- ".join(contents)

# Classification tool
@rottermaatje_agent.tool
async def get_triage_info(ctx: RunContext[AgentDeps]) -> str:
    """
    Get the triage classification for the current user input.
    Always call this first to understand topic, language, emergency status, and sensitivity.
    """
    async with cl.Step(name="Triage-analyse", type="tool"):
        if ctx.deps.triage_data:
            td = ctx.deps.triage_data
            return f"Triage: Topic='{td.topic}', Language='{td.language}', Emergency={td.is_emergency}, Disclaimer='{td.disclaimer_type}'. Reason: {td.reasoning}"
        return "No triage data."