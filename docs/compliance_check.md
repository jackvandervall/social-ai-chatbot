# Compliance Check: RotterMaatje 2.0 Requirements

**Date:** 2026-01-18
**Status:** 🏗️ Partially Compliant

This document compares the current codebase against `01_requirements.md`.

## ✅ Implemented Features

### 1. Doel & Context / 2. Ontwerpprincipes
- **Menselijk contact centraal:** System prompts explicitly state the bot supports but does not replace humans.
- **Veiligheid/Grenzen:** Triage agent detects emergencies and blocks interaction if needed (step 2 in `app.py`).

### 3. Functionele Vaardigheden
- **3.1 Informatieverstrekking:** RAG system implemented with `pgvector`. Data ingestion for APV and FAQ structured data is complete.
- **3.2 Doorverwijzing:** Disclaimers configured in `PromptConfig` point to specific organizations (Juridisch Loket, etc.).
- **3.3 Triage:** `TriageAgent` classifies Topic, Language, and Emergency status.
- **3.4 Rolbewust gedrag:** "Context Mode" switch (Volunteer vs. Direct) implemented in `app.py` settings. Distinct system prompts for each mode.
- **3.5 Grenzen bewaken:** "Safety Check" step visible in UI. Emergency blocker active.

### 4. Kennisdomein
- **Fact-based:** `ingest_knowledge.py` enables structured data ingestion.
- **Hallucination checks:** Prompts instruct "If uncertain, acknowledge it".

### 5. Communicatiestijl
- **B1 Level:** Instructed in system prompts.
- **Tone:** Instructed to be empathetic, no humor, respectful.
- **Privacy:** System prompt forbids asking for BSN/full names.

### 6. Taalvaardigheid
- **Multilingual Support:** Triage detects language. Translation buttons added for Polish, Arabic, English. Model instructed to reply in user's language.

### 8. Veiligheid & Ethiek
- **No medical/legal advice:** Explicitly forbidden in system prompts.
- **Emergency handling:** 112 referral implemented in `app.py` and `prompts.py`.

---

## ❌ Missing / Incomplete Requirements

### 7. Toegankelijkheid (Accessibility)
This section is the primary gap in the current implementation.

1.  **Audiofunctie (TTS)**
    *   **Requirement:** "Mogelijkheid om tekst voor te laten lezen."
    *   **Status:** **Missing.** No Text-to-Speech (TTS) integration found in `app.py`.

2.  **Pictogrammen / Visuele Ondersteuning**
    *   **Requirement:** "Pictogrammen voor kernonderwerpen (eten, slapen, zorg, post, veiligheid)."
    *   **Status:** **Partial/Missing.** The Triage step text shows the topic, but there are no dedicated visual icons or cards for these topics in the chat interface.

3.  **Interface Language**
    *   **Observation:** The UI (Welcome message, "Safety Check" label) is hardcoded in English. For a tool targeted at Rotterdam (mostly Dutch speakers + migrants), the interface shells should likely be localized or at least Dutch by default.

---

## Recommendations
1.  **Implement TTS:** Add an "Audio" button to messages using Chainlit's audio capabilities or an external API (ElevenLabs/OpenAI TTS).
2.  **Add Visuals:** Use Chainlit Elements (Images/Cards) to show icons for the detected topic (e.g., a bed icon for 'shelter').
3.  **Localize UI:** Translate the Welcome Message and Step names to Dutch (or make them dynamic based on detected language).
