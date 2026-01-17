import sys
import os
import chainlit as cl

# Fix path to import modules from parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.chatbot import rottermaatje_agent, AgentDeps
from services.pgvectordb import VectorDB
from core.prompts import PromptConfig
from agents.triage import triage_agent, TriageStatus

from core.llm import get_model
from pydantic_ai import Agent

# Initialize Database once on startup
db = VectorDB()

async def translate_text(text: str, target_language: str) -> str:
    """Helper function to translate text using the configured LLM."""
    try:
        agent = Agent(get_model())
        prompt = f"Translate the following text to {target_language}. Return ONLY the direct translation, nothing else:\n\n{text}"
        result = await agent.run(prompt)
        return result.output
    except Exception as e:
        return f"Translation failed: {str(e)}"

@cl.action_callback("translate_pl")
async def translate_to_polish(action: cl.Action):
    translated = await translate_text(action.payload["text"], "Polish")
    await cl.Message(content=f"**🇵🇱 Polski:**\n{translated}").send()

@cl.action_callback("translate_ar")
async def translate_to_arabic(action: cl.Action):
    translated = await translate_text(action.payload["text"], "Arabic")
    await cl.Message(content=f"**🇸🇦 العربية:**\n{translated}").send()

@cl.action_callback("translate_en")
async def translate_to_english(action: cl.Action):
    translated = await translate_text(action.payload["text"], "English")
    await cl.Message(content=f"**🇬🇧 English:**\n{translated}").send()

@cl.on_chat_start
async def start():
    """
    Initialize the chat session and send a welcome message.
    This function is triggered when a new chat session starts. It sends
    an introductory message to the user explaining the bot's purpose.
    """
    welcome_msg = """
    **Welkom bij RotterMaatje 2.0** 👋
    
    Ik ben er om je te helpen met informatie over opvang, medische zorg en procedures.
    *Typ een vraag om te beginnen.*
    """
    await cl.Message(content=welcome_msg).send()

@cl.on_message
async def main(message: cl.Message):
    """
    Execute the main chat loop for incoming messages.
    This handler orchestrates the following steps:
    1. Runs the Triage Agent to classify the input (Topic, Language, Emergency).
    2. Updates the UI with a visual 'Safety Check' step.
    3. Checks for emergencies and displays a blocker if necessary.
    4. Runs the Main Agent with streaming response capabilities.
    5. Handles fallback for models that use tool returns instead of streaming.
    6. Post-processes the response to append necessary disclaimers.

    Args:
        message (cl.Message): The incoming message object from the user.
    """
    user_input = message.content

    # --- STEP 1: VISUAL TRIAGE ---
    async with cl.Step(name="Veiligheidscheck", type="tool") as step:
        step.input = user_input
        # Run Triage Agent
        triage_result = await triage_agent.run(user_input)
        status: TriageStatus = triage_result.output
        
        # Update the UI step with the reasoning
        step.output = (
            f"Topic: {status.topic} | "
            f"Language: {status.language} | "
            f"Emergency: {status.is_emergency}\n"
            f"Reasoning: {status.reasoning}"
        )

    # --- STEP 2: EMERGENCY BLOCKER ---
    if status.is_emergency:
        emergency_msg = (
            f"🚨 **NOODGEVAL DETECTIE**\n\n"
            f"{PromptConfig.get_disclaimer(status.disclaimer_type)}"
        )
        await cl.Message(content=emergency_msg, author="RotterMaatje").send()
        return  # Stop here for emergencies

    # --- STEP 3: MAIN AGENT WITH STREAMING ---
    deps = AgentDeps(db=db, triage_data=status)
    
    # Create empty message for streaming
    msg = cl.Message(content="")
    await msg.send()

    # Stream the response
    response_text = ""
    async with rottermaatje_agent.run_stream(user_input, deps=deps) as result:
        async for chunk in result.stream_text(delta=True):
            response_text += chunk
            await msg.stream_token(chunk)
        
        # Handle silent tool returns
        if not response_text:
            final_data = await result.get_output()
            if final_data:
                response_text = str(final_data)
                await msg.stream_token(response_text)

    # --- STEP 4: ADD DISCLAIMER AFTER RESPONSE ---
    if status.disclaimer_type != 'none':
        disclaimer = PromptConfig.get_disclaimer(status.disclaimer_type)
        # Append disclaimer AFTER the agent response
        final_response = response_text + "\n\n" + disclaimer
    else:
        final_response = response_text

    # Update message with final content including disclaimer
    # Update message with final content including disclaimer
    msg.content = final_response
    
    # Add translation actions
    actions = [
        cl.Action(name="translate_pl", payload={"text": final_response}, label="🇵🇱 Polski"),
        cl.Action(name="translate_ar", payload={"text": final_response}, label="🇸🇦 العربية"),
        cl.Action(name="translate_en", payload={"text": final_response}, label="🇬🇧 English"),
    ]
    msg.actions = actions
    
    await msg.update()