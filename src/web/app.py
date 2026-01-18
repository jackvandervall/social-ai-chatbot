import sys
import os
import chainlit as cl
from chainlit.input_widget import Select

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

@cl.on_settings_update
async def on_settings_update(settings):
    """Handle settings updates from the chat UI."""
    context_mode = settings.get("context_mode", "volunteer")
    cl.user_session.set("context_mode", context_mode)
    
    # Notify user of mode change
    mode_name = "Volunteer Mode" if context_mode == "volunteer" else "Direct Mode (Homeless Person)"
    await cl.Message(content=f"✅ Switched to **{mode_name}**").send()

@cl.on_chat_start
async def start():
    """
    Initialize the chat session and send a welcome message.
    This function is triggered when a new chat session starts. It sends
    an introductory message to the user explaining the bot's purpose.
    """
    # Initialize context mode in session
    cl.user_session.set("context_mode", "volunteer")
    
    # Set up chat settings with context mode dropdown
    settings = await cl.ChatSettings(
        [
            Select(
                id="context_mode",
                label="Communicatiemodus",
                values=["volunteer", "direct"],
                initial_index=0,
                description="Schakel tussen vrijwilligers- en directe modus"
            )
        ]
    ).send()
    
    welcome_msg = """
**Welkom bij RotterMaatje 2.0** 👋

Ik ben hier om je te helpen met informatie over opvang, medische zorg en procedures in Rotterdam.

**💡 Tip:** Gebruik het ⚙️ instellingenmenu om te schakelen tussen:
- **Vrijwilligersmodus**: Voor vrijwilligers die daklozen helpen.
- **Directe modus**: Spreekt direct tegen de persoon in nood.

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
    # Get initial user input
    user_input = message.content or ""
    
    # --- HANDLE FILE UPLOADS ---
    # Extract text from uploaded files (e.g., .txt, .md, .json, .csv)
    file_contents = []
    MAX_FILE_CHARS = 50000  # Safety limit for total injected text
    
    if message.elements:
        for element in message.elements:
            # Check for text-based file extensions
            supported_extensions = (".txt", ".md", ".json", ".csv", ".log")
            if element.type == "file" and element.name.lower().endswith(supported_extensions):
                try:
                    # Chainlit saves uploaded files to a temporary path
                    with open(element.path, "r", encoding="utf-8") as f:
                        content = f.read()
                        
                        # Apply a per-file limit to prevent context window overflow
                        if len(content) > MAX_FILE_CHARS:
                            content = content[:MAX_FILE_CHARS] + "\n... [Inhoud ingekort wegens lengte] ..."
                        
                        file_contents.append(f"📄 **Bestand: {element.name}**\n---\n{content}\n---")
                except Exception as e:
                    file_contents.append(f"⚠️ Fout bij het lezen van {element.name}: {str(e)}")
    
    # If files were uploaded, append them to the user input
    if file_contents:
        header = "### 📎 GEÜPLOADE DOCUMENTEN\nDe gebruiker heeft documenten bijgevoegd voor context. Gebruik de onderstaande informatie om de vraag te beantwoorden:\n\n"
        # If the user didn't provide text, give it a default context
        if not user_input.strip():
            user_input = "Ik heb documenten geüpload. Zie de bijlagen voor details."
        
        user_input += "\n\n" + header + "\n\n".join(file_contents)
    
    # Get context mode from session
    context_mode = cl.user_session.get("context_mode", "volunteer")

    # --- STEP 1: VISUAL TRIAGE ---
    async with cl.Step(name="Veiligheidscontrole") as step:
        # Run Triage Agent
        triage_result = await triage_agent.run(user_input)
        status: TriageStatus = triage_result.output
        
        # Map topics to readable Dutch categories with icons
        topic_map = {
            "shelter": "🛌 Slapen / Opvang",
            "medical": "🏥 Medische hulp / Zorg",
            "food": "🍴 Eten & Drinken",
            "legal": "📄 Juridisch / Documenten",
            "social": "🤝 Sociaal / Welzijn",
            "other": "❓ Overig"
        }
        category = topic_map.get(status.topic, f"❓ {status.topic}")

        # Map languages to names
        lang_map = {"nl": "Nederlands", "en": "Engels", "pl": "Pools", "ar": "Arabisch"}
        language = lang_map.get(status.language, status.language.upper())

        # Update the UI step with formatted output
        step.output = (
            f"**Categorie:** {category}\n"
            f"**Taal:** {language}\n"
            f"**Spoed:** {'🚨 JA' if status.is_emergency else '✅ Geen spoed'}\n\n"
            f"**Analyse:** {status.reasoning}"
        )

    # --- STEP 2: EMERGENCY BLOCKER ---
    if status.is_emergency:
        emergency_msg = (
            f"🚨 **EMERGENCY DETECTED**\n\n"
            f"{PromptConfig.get_disclaimer(status.disclaimer_type)}"
        )
        await cl.Message(content=emergency_msg, author="RotterMaatje").send()
        return  # Stop here for emergencies

    # --- STEP 3: MAIN AGENT WITH STREAMING ---
    deps = AgentDeps(db=db, triage_data=status, context_mode=context_mode)
    
    # Create empty message for streaming
    msg = cl.Message(content="")
    
    # Use a step to show "thinking" until we get the first chunk
    async with cl.Step(name="Hulpbronnen raadplegen...") as thinking_step:
        # Stream the response
        response_text = ""
        async with rottermaatje_agent.run_stream(user_input, deps=deps) as result:
            # We want to close the thinking step as soon as we start getting content
            first_chunk = True
            async for chunk in result.stream_text(delta=True):
                if first_chunk:
                    thinking_step.output = "Antwoord verzonden."
                    await msg.send()
                    first_chunk = False
                
                response_text += chunk
                await msg.stream_token(chunk)
            
            # Handle silent tool returns (if no text was streamed)
            if not response_text:
                final_data = await result.get_output()
                if final_data:
                    response_text = str(final_data)
                    await msg.send()
                    await msg.stream_token(response_text)

    # --- STEP 4: ADD DISCLAIMER AFTER RESPONSE ---
    if status.disclaimer_type != 'none':
        disclaimer = PromptConfig.get_disclaimer(status.disclaimer_type)
        # Append disclaimer AFTER the agent response
        final_response = response_text + "\n\n" + disclaimer
    else:
        final_response = response_text

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
