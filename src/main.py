import asyncio
import os
from dotenv import load_dotenv
from agent import rotter_agent, AgentDeps
from database import VectorDB 

# Load .env variables
load_dotenv()

async def main():
    # Initialize dependencies
    db = VectorDB()
    deps = AgentDeps(db=db)
    
    print("--- Rottermaatje 2.0 (Terminal Mode) ---")
    print("Type 'exit' om te stoppen.\n")

    # Start conversation loop
    while True:
        user_input = input("Gebruiker: ")
        if user_input.lower() in ["exit", "stop", "quit"]:
            break

        try:
            # Run the Pydantic AI Agent
            result = await rotter_agent.run(user_input, deps=deps)
            
            # Print the response (use .output instead of .data)
            print(f"Rottermaatje: {result.output}\n")
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())