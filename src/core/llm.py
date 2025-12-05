import os
from dotenv import load_dotenv

load_dotenv()

MODEL_PROVIDER = os.getenv('MODEL_PROVIDER', 'openrouter')

def get_model():
    """
    Returns the model configuration based on MODEL_PROVIDER.
    """
    if MODEL_PROVIDER == 'local':
        return 'openai:qwen/qwen3-4b-2507'
    elif MODEL_PROVIDER == 'openrouter':
        OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
        if not OPENROUTER_API_KEY:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables")
        return 'openrouter:deepseek/deepseek-v3.2'
    else:
        raise ValueError(f"Invalid MODEL_PROVIDER: {MODEL_PROVIDER}. Must be 'openrouter' or 'local'")