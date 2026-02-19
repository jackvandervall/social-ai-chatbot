import os
from dotenv import load_dotenv
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

load_dotenv()

MODEL_PROVIDER = os.getenv('MODEL_PROVIDER', 'openrouter')

# For local, set MODEL_PROVIDER to 'local' in .env
# For OpenRouter API, set MODEL_PROVIDER to 'openrouter' in .env
def _get_api_key():
    OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY not found in environment variables")
    return OPENROUTER_API_KEY

def _get_openrouter_model(model_name: str) -> OpenAIChatModel:
    """
    Creates an OpenAI-compatible model pointing to OpenRouter's API.
    This bypasses PydanticAI's OpenRouterModel which has a validation bug
    with upstream_inference_cost expecting int instead of float.
    """
    return OpenAIChatModel(
        model_name,
        provider=OpenAIProvider(
            base_url='https://openrouter.ai/api/v1',
            api_key=_get_api_key(),
        ),
    )

def get_model():
    """
    Returns the primary model configuration.
    """
    if MODEL_PROVIDER == 'local':
        return 'openai:qwen/rottermaatje-qwen3-4b-dpo'
    elif MODEL_PROVIDER == 'openrouter':
        return _get_openrouter_model('google/gemini-3-flash-preview')
    else:
        raise ValueError(f"Invalid MODEL_PROVIDER: {MODEL_PROVIDER}. Must be 'openrouter' or 'local'")

def get_triage_model():
    """
    Returns a cheap and fast model for triage classification.
    """
    if MODEL_PROVIDER == 'local':
        return 'openai:qwen/rottermaatje-qwen3-4b-dpo'
    elif MODEL_PROVIDER == 'openrouter':
        return _get_openrouter_model('openai/gpt-oss-safeguard-20b')
    else:
        raise ValueError(f"Invalid MODEL_PROVIDER: {MODEL_PROVIDER}. Must be 'openrouter' or 'local'")