import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ConfigDict
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIChatModel
from database import VectorDB

# Load environment variables
load_dotenv()

# CRITICAL: Set up OpenRouter configuration
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY not found in environment variables")

# 1. DEFINE STRUCTURED TRIAGE
class TriageStatus(BaseModel):
    """
    Represents the urgency and categorization of a user's input.
    Attributes:
        is_emergency (bool): Indicates if the situation is life-threatening.
        topic (str): The specific category of help needed.
        language_detected (str): The ISO code of the detected language.
    """
    is_emergency: bool = Field(
        False, description="Is this a life-threatening situation (911/112)?"
    )
    topic: str = Field(
        ..., description="Category: 'shelter', 'medical', 'legal', 'food', 'other'"
    )
    language_detected: str = Field(
        ..., description="Language code: nl, en, pl, ar"
    )

# 2. DEFINE DEPENDENCIES
class AgentDeps(BaseModel):
    """
    Defines the dependencies required by the agent during execution.
    Attributes:
        db (VectorDB): The vector database instance for RAG operations.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)
    db: VectorDB

# 3. DEFINE THE AGENT
# Configure OpenRouter with DeepSeek
# Note: When using provider='openrouter', you can pass the full model string
rotter_agent = Agent(
    model='openrouter:deepseek/deepseek-v3.2',  # Shorthand notation
    deps_type=AgentDeps,
    system_prompt=(
        "You are a helpful assistant called Rottermaatje for homeless people in Rotterdam."
        "Analyze user queries and categorize them appropriately."
        "Detect the language and determine urgency levels."
    )
)

# 4. DEFINE TOOLS (RAG)
@rotter_agent.tool
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
    results = await ctx.deps.db.search(query)
    if not results:
        return "Geen specifieke informatie gevonden in de database."
    return "- " + "\n- ".join(results)