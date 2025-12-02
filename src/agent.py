import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ConfigDict
from pydantic_ai import Agent, RunContext
from database import VectorDB
from prompts import PromptConfig

# Load environment variables
load_dotenv()

# CRITICAL: Set up OpenRouter configuration
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY not found in environment variables")

# DEFINE DEPENDENCIES
class AgentDeps(BaseModel):
    """
    Defines the dependencies required by the agent during execution.
    Attributes:
        db (VectorDB): The vector database instance for RAG operations.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)
    db: VectorDB

# DEFINE THE AGENT
rottermaatje_agent = Agent(
    model='openrouter:deepseek/deepseek-v3.2',
    deps_type=AgentDeps,
    system_prompt=PromptConfig.get_system_prompt(),
)

# DEFINE TOOLS (RAG)
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
    results = await ctx.deps.db.search(query)
    if not results:
        return "Geen specifieke informatie gevonden in de database."
    return "- " + "\n- ".join(results)