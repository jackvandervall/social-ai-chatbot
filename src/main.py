import asyncio
import os
from typing import Optional
from dotenv import load_dotenv
from agent import rottermaatje_agent, AgentDeps
from database import VectorDB 
from prompts import PromptConfig

# Load .env variables
load_dotenv()

class GuardrailsManager:
    """Centralized guardrails management."""
    
    @staticmethod
    async def pre_process(user_input: str) -> Optional[str]:
        """
        Pre-processing checks. Returns error message if input should be blocked.
        Returns None if input passes all checks.
        """
        # Check 1: Empty input
        if not user_input.strip():
            return "Je bericht is leeg. Typ iets om te beginnen."
        
        # Check 2: Input too long
        if len(user_input) > 1000:
            return "Je bericht is te lang. Probeer het in kortere delen op te splitsen."
        
        # Check 3: Spam detection (repeated characters with less than three being unique)
        if len(set(user_input)) < 3 and len(user_input) > 10:
            return "Dit lijkt geen geldige vraag te zijn."
        
        return None  # All checks passed
    
    @staticmethod
    async def detect_emergency(user_input: str) -> bool:
        """Detect if input contains emergency keywords."""
        return PromptConfig.check_emergency_keywords(user_input)
    
    @staticmethod
    async def post_process(response: str, user_input: str) -> str:
        """
        Post-processing modifications to agent response.
        """
        # Add emergency banner if needed
        if await GuardrailsManager.detect_emergency(user_input):
            emergency_banner = f"\n\n🚨 {PromptConfig.SAFETY_DISCLAIMERS['emergency']}"
            response = emergency_banner + "\n\n" + response
        
        # Truncate if max_length is set
        max_length = PromptConfig.GUARDRAILS["max_response_length"]
        if max_length is not None and len(response) > max_length:
            response = response[:max_length] + "...\n\n(Antwoord ingekort)"        
            
        return response

# Run agent with pre- and post-processing guardrails
async def main():
    db = VectorDB()
    deps = AgentDeps(db=db)
    guardrails = GuardrailsManager()
    
    print("--- Rottermaatje 2.0 (Terminal Mode) ---")
    print("Type 'exit' om te stoppen.\n")
    
    while True:
        user_input = input("Gebruiker: ")
        if user_input.lower() in ["exit", "stop", "quit"]:
            print("Tot ziens!")
            break
        
        try:
            # PRE-PROCESSING GUARDRAILS
            error_msg = await guardrails.pre_process(user_input)
            if error_msg:
                print(f"Rottermaatje: {error_msg}\n")
                continue
            
            # Run agent
            result = await rottermaatje_agent.run(user_input, deps=deps)
            
            # POST-PROCESSING GUARDRAILS
            final_response = await guardrails.post_process(
                result.output, 
                user_input
            )
            
            print(f"Rottermaatje: {final_response}\n")
            
        except Exception as e:
            print(f"Error: {e}\n")

if __name__ == "__main__":
    asyncio.run(main())