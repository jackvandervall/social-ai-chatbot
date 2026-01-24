import os
from dotenv import load_dotenv

load_dotenv()

MODEL_PROVIDER = os.getenv('MODEL_PROVIDER', 'openrouter')

# For local, set MODEL_PROVIDER to 'local' in .env
# For OpenRouter API, set MODEL_PROVIDER to 'openrouter' in .env
def _get_api_key():
    OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY not found in environment variables")
    return OPENROUTER_API_KEY

def get_model():
    """
    Returns the primary model configuration.
    """
    if MODEL_PROVIDER == 'local':
        return 'openai:qwen/rottermaatje-qwen3-4b-dpo'
    elif MODEL_PROVIDER == 'openrouter':
        _get_api_key() # Verify key exists
        return 'openrouter:x-ai/grok-4.1-fast'
    else:
        raise ValueError(f"Invalid MODEL_PROVIDER: {MODEL_PROVIDER}. Must be 'openrouter' or 'local'")

def get_triage_model():
    """
    Returns a cheap and fast model for triage classification.
    """
    if MODEL_PROVIDER == 'local':
        return 'openai:qwen/rottermaatje-qwen3-4b-dpo'
    elif MODEL_PROVIDER == 'openrouter':
        _get_api_key() # Verify key exists
        return 'openrouter:openai/gpt-oss-safeguard-20b'
    else:
        raise ValueError(f"Invalid MODEL_PROVIDER: {MODEL_PROVIDER}. Must be 'openrouter' or 'local'")