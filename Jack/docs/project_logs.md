## Daily Logs
---
**27-11-2025**
Initiële setup met gebruikerspecifieke en gezamenlijke folderstructuur en uv packet manager initialisatie voor efficiënt beheer van libraries.

**01-12-2025**
example_evaluating_llm.ipynb en environment variabelen aangepast zodat ik CUDA kon gebruiken om llm's op mijn gpu te kunnen runnen. Verder nog verschillende prompts getest op de 3 llm's in de example Python file: QWEN3: 0.6, 0.6-base en 4B. Daarnaast een proof-of-concept agent met basic system prompt en mock database aangemaakt.

**02-12-2025**
Proof-of-concept agent.py aangepast om deepseek/deepseek-v3.2 te gebruiken, getest op verschillende talen als Engels, Nederlands, Arabisch en Pools waaruit blijkt dat dit model een goed begrip heeft van diverse talen. Dit model heeft ook een ruime context window van 163K, helaas is het niet mogelijk om dit te fine-tunen vanwege de grootte van het model, maar we zouden het kunnen gebruiken als testmodel om later een gedistilleerd deepseek model te fine-tunen zoals deepseek-r1-distill-llama-8b of deepseek-r1-distill-qwen-32b.

Om de agent te voorzien van een robuuste system prompt, guardrails en veiligheidsdisclaimers is de prompts.py file aangemaakt. De prompts.py file heeft de volgende voordelen:

- Versiebeheer: Track prompt aanpassingen los van de agent architecture
- A/B Testing: Gemakkelijk prompt configuraties testen en vergelijken
- Snelle iteratie: Update prompts zonder de code te hoeven aanpassen

**04-12-2025**
Projectoverleg met de groep en Rachid, hieruit hebben wij positieve feedback gekregen op onze voortgang en tips om lokale LLM's te testen door middel van LM Studio, daarnaast hebben we tool usage besproken en zijn we van plan om MCP's te gebruiken. We zullen de regels van de tool usage in de system prompt beschrijven.

We hebben diverse modellen getest in LM Studio:
- qwen/qwen3-vl-4b: Werkt erg snel, alleen valt het model vaak in loops waardoor het gaat hallucineren, de context van dit model is tevens erg klein waardoor ik beter een model met grotere context window kan proberen. Was een staff-pick op LM Studio, maar ik kwam erachter dat het specifiek getraint is op visual perception, spatial reasoning, and image understanding.

- qwen/qwen3-4b-2507: Werkt erg snel, valt minder vaak in loops, maar maakt grammaticale fouten in Nederlands en de kwaliteit van responses kan beter.

- qwen/qwen3-8b: Outputkwaliteit beter dan qwen3-4b, maar kan de ontwikkeling hinderen door trage output op mijn gpu.

- deepseek/deepseek-r1-0528-qwen3-8b: Van de geteste modellen de beste outputs, gelijke performance aan Qwen3-235B-thinking wat extreem goed is voor zo'n klein model, maar is door de combinatie van Chain-of-Thought reasoning met lage tokens per seconde op mijn gpu erg traag voor development en iteratief testen.

We hebben de guardrails gehardcoded in de prompts.py, maar dit kan problemen veroorzaken zoals wanneer een gebruiker een spelfout maakt: "drugsgebruik" als "drugs gebruik", de context niet begrijpt, wat false positives aangeeft: "ik lees een boek over drugsgebruik" of een negatie ziet als positive: "ik denk niet aan drugsgebruik". Om dit te voorkomen kunnen we een Triage Agent implementeren die eerst de gebruikersinput analyseert voor begrip van intentie.

De triage agent zal inputs labelen zoals is_emergency, topic, language, reasoning etc. wat daarnaast ook inzichten zou kunnen geven aan interacties wat in de toekomst de optimalisatie kan ondersteunen en zo de kwaliteit van verschillende LLM's en system prompts gekwantificeerd kunnen worden.

**05-12-2025**
- Chainlit getest op de chatbot, UI ziet er goed uit en biedt mogelijkheden tot personalisatie zoals extra buttons voor de gebruikers.
- README.md geüpdatet op basis van de huidige architecture.
- Tijdens het gebruik van tools werd de agent door gestructureerde data verward over zijn eigen identiteit, waardoor hij outputs in verkeerde JSON format ging outputten, hierdoor werd de response onjuist gestreamed naar Chainlit.

**11-12-2025**
VectorDB opgezet en de FAQ embeddings gemaakt met een n8n workflow en openai/text-embedding-3-small, inclusief combined_text en metadata zoals: categorie, doelgroep, trefwoorden, bron_vraag en source_type.

**12-01-2026**
Begin aan fine-tuning code voor Qwen3-8B, gekozen voor Supervised Fine-Tuning (SFT) met Unsloth framework, vanwege de 2x snellere training dan standaard Hugging Face en 70% minder VRAM-gebruik door kernel-optimalisaties. 

**13-01-2026**
Verder gewerkt aan de fine-tuning code. Daarnaast als Reinforcement Learning framework, gekozen voor parameter-efficient fine-tuning (PEFT) met LoRA (Low-Rank Adaptation) in plaats van volledige fine-tuning, zodat het mogelijk is om het model te trainen op een consumer hardware zoals een RTX 3060 6GB. Persoonlijk heb ik een GTX 3040 4GB, dus ik kan geen volledige fine-tuning doen of moet overstappen op Qwen2.5-3B-Instruct, ~3.2 GB, goede kwaliteit met multilingual support. Waarschijnlijk ga ik kijken naar een betere LLM die ik kan trainen in een cloud-omgeving zoals Google Colab of van Hogeschool Rotterdam Datalab.