import asyncio
import os
from typing import Optional
from dotenv import load_dotenv
from src.agents.chatbot import rottermaatje_agent, AgentDeps
from src.services.pgvectordb import VectorDB
from src.core.prompts import PromptConfig
from src.agents.triage import triage_agent, TriageStatus

# Load .env variables
load_dotenv()


async def basic_pre_checks(user_input: str) -> Optional[str]:
    """Basic input validation."""
    if not user_input.strip():
        return "Je bericht is leeg. Typ iets om te beginnen."
    if len(user_input) > 1000:
        return "Je bericht is te lang. Probeer het in kortere delen op te splitsen."
    if len(set(user_input)) < 3 and len(user_input) > 10:
        return "Dit lijkt geen geldige vraag te zijn."
    return None


async def main():
    db = VectorDB()
    print("--- Rottermaatje 2.0 (Terminal Mode) ---")
    print("Type 'exit' om te stoppen.\n")

    while True:
        user_input = input("Gebruiker: ")
        if user_input.lower() in ["exit", "stop", "quit"]:
            print("Tot ziens!")
            break

        # Basic pre-checks
        error_msg = await basic_pre_checks(user_input)
        if error_msg:
            print(f"Rottermaatje: {error_msg}\n")
            continue

        # Triage step
        triage_result = await triage_agent.run(user_input)
        status: TriageStatus = triage_result.output

        # Print triage summary
        print(f"[Triage] Topic: {status.topic}, Language: {status.language}, Emergency: {status.is_emergency}, Disclaimer: {status.disclaimer_type}")
        print(f"[Reasoning] {status.reasoning}\n")

        # If emergency, show alert and optionally block
        if status.is_emergency:
            disclaimer = PromptConfig.get_disclaimer(status.disclaimer_type)
            if disclaimer:
                print(f"Rottermaatje: {disclaimer}\n")

        # Prepare dependencies for main agent (including triage data)
        deps = AgentDeps(db=db, triage_data=status)

        # Run main agent
        result = await rottermaatje_agent.run(user_input, deps=deps)

        final_response = result.output
        if status.disclaimer_type != 'none':
            disclaimer = PromptConfig.get_disclaimer(status.disclaimer_type)
            final_response = disclaimer + "\n\n" + final_response

        print(f"Rottermaatje: {final_response}\n")


if __name__ == "__main__":
    asyncio.run(main())