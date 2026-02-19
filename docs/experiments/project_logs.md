## Daily Logs

### November 2025
**27-11-2025**
Initiële setup met gebruikerspecifieke en gezamenlijke folderstructuur en uv packet manager initialisatie voor efficiënt beheer van libraries.

### December 2025

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

### January 2026

**12-01-2026**
Begin aan fine-tuning code voor Qwen3-8B, gekozen voor Supervised Fine-Tuning (SFT) met Unsloth framework, vanwege de 2x snellere training dan standaard Hugging Face en 70% minder VRAM-gebruik door kernel-optimalisaties.

> 📖 **Technische details:** Zie [Verantwoording Fine-Tuning](./verantwoording_fine-tuning.md) voor uitgebreide documentatie over de trainingsparameters en architectuur.

**13-01-2026**
Verder gewerkt aan de fine-tuning code, ik heb gekozen voor parameter-efficient fine-tuning (PEFT) met LoRA (Low-Rank Adaptation) in plaats van volledige fine-tuning, zodat het mogelijk is om het model te trainen op een consumer hardware zoals een RTX 3060 6GB. Persoonlijk heb ik een GTX 3050 4GB, dus ik kan geen volledige fine-tuning doen of moet overstappen op Qwen2.5-3B-Instruct, ~3.2 GB, goede kwaliteit met multilingual support. Waarschijnlijk ga ik kijken naar een betere LLM die ik kan trainen in een cloud-omgeving zoals Google Colab of van Hogeschool Rotterdam Datalab.

Voor de Reinforcement Learning (RL) heb ik gekozen voor Direct Preference Optimization (DPO), omdat het stabieler en efficiënter is dan traditionele RLHF, directe optimalisatie van gebruikersvoorkeuren mogelijk maakt zonder complex reward model, en naadloos integreert met Unsloth voor snelle training op hardware met beperkt VRAM.

> 🔧 **Hardware motivatie:** Zie [LLM Verantwoording](./llm_verantwoording.md) voor de volledige onderbouwing van de modelkeuze.

**17-01-2026**
Aanpassingen gedaan aan de agent, namelijk een vertalingsfunctie op het advies van de chatbot, zodat de vrijwilligers de adviezen in de taal van de dakloze kunnen laten lezen. Daarnaast een gebruikersinstructie in de 'Leesmij' knop op de frontend. De system prompts zijn nu dynamisch en worden aangepast op basis van de type gebruiker, 'volunteer' of 'direct'.

Voor veiligheidsredenen heb ik guardrails gemaakt zodat de chatbot nooit naar een volledige naam, BSN, of gevoelige persoonsgegevens zal vragen. Daarnaast zijn er overige instanties bijgevoegd aan de safety disclaimers van de triage agent, inclusief links naar de instanties voor real-time verificatie. 

Tot slot heb ik relevante gegevens uit de Algemeen Plaatselijke Verordening (APV) van de gemeente Rotterdam, gehaald en in de vector database toegevoegd. Hier staan regels over openbare orde en veiligheid, verkeerszaken en horeca-aangelegenheden. Hier is een algemene script voor gemaakt zodat ik van meerdere bronnen soortgelijke informatie kan importeren en in de vector database toevoegen. 

Hoe ik de data structureer voor de vector database, is door de html code te parseren door een LLM (Google Gemini Pro 3), met de volgende prompt:

Extract alle informatie die toepasselijk is op dak- en thuisloze personen.

Verander het daarna in een vraag en antwoord format:

```json
[
  {
    "vraag": "Waarom word ik aangesproken als ik met een groepje op straat sta?",
    "antwoord": "Dit valt onder 'Openbare Ordeverstoring' (Woonoverlast & Straatoverlast). De politie grijpt in bij gedrag dat de rust verstoort, zoals groepsvorming, schreeuwen of ingangen blokkeren. Meldingen hiervan zijn de laatste jaren verdubbeld.",
    "metadata": {
      "categorie": "Openbare Orde",
      "doelgroep": "cliënt",
      "trefwoorden": ["overlast", "groepsvorming", "APV", "politiecontact"]
    }
  }
]
```

Met deze data kan de chatbot door middel van de pgvector tool gemakkelijk de juiste informatie vinden, door de implementatie van een vector database is dit erg schaalbaar.

**18-01-2026**
Om de triage van de gebruikers input classificatie te versnellen en kostenefficiënter te maken heb ik ervoor gekozen om in llm.py de gebruikte llm op te splitsen. Voor classificatie heb ik gekozen voor een API call naar Openrouter met gpt-oss-safeguard-20b, het een safety reasoning model van OpenAI, gebouwd op basis van gpt-oss-20b. Dit is een Mixture-of-Experts (MoE) model met lower latency (goed voor triage), gemaakt voor veiligheidstaken zoals content classification, LLM filtering, en trust & safety labeling. Met deze setup worden de juiste safety disclaimers gegeven en kan er tijdens een noodgeval de chat stopgezet worden, om de gebruiker direct op de hoogte te stellen van de ernst van de situatie zodat hulpdiensten z.s.m. ingeschakeld kunnen worden. (Voorbeeld: "De cliënt voelt pijn op de borst", wat kan duiden op een hartaanval)

Naast het aanpassen van de triage agent, heb ik ook de bestandupload functionaliteit geïmplementeerd, hierdoor kunnen vrijwilligers intakeformulieren laten invullen en versturen voor de juiste verwijzing naar hulpinstanties. Ik heb dit uitgetest door een intakeformulier te genereren met Google Gemini Pro 3, en deze te uploaden via de frontend. Hierdoor kan de chatbot de juiste informatie uit het formulier halen en de vrijwilliger de juiste adviezen geven.

> 📋 **Testcasus:** Zie [Casus "Jonathan" (Alcohol & Dakloosheid)](./findings/test_casus_intakeformulier.md) voor een uitgebreide analyse van de chatbot-interactie en effectiviteitsbeoordeling.

**19-01-2026**
Vandaag heb ik data gegenereerd om het qwen3-4b-instruct model te fine-tunen. Om de data te generenen heb ik Deepseek V3.2 gebruikt voor data-generatie vanwege lage kosten en meertalige kracht. De data is gegenereerd op basis van reële interacties en topics vanuit de data in de interne kennisbank. Daarnaast is ook DPO reinforcement learning toegepast, waardoor de LLM ook leert om een foutieve toon en incorrecte data te vermijden. Zelfs met quantization kon ik het niet lokaal trainen, vanwege deze error:

>"ValueError: Some modules are dispatched on the CPU or the disk. Make sure you have enough GPU RAM to fit the quantized model."

Vandaar dat ik het via Google Colab heb gedaan.

Zoals te zien is uit de test output, geeft het model op empathische manier antwoord. Er is alleen een merkwaardig antwoord gegenereerd, waarin de LLM ervan uit lijkt te gaan dat de user uit de gevangenis komt, in tegenstelling tot de initiële prompt, waarbij de user dakloos is en honger heeft. Dit kan komen door de data die is gebruikt voor het fine-tunen, waarbij er ook data is gebruikt over mensen die uit de gevangenis komen, mogelijke overtraining heeft voor deze hallucinatie gezorgt. Het is belangrijk om diverse data te hebben voor het fine-tunen om deze bias te voorkomen.

> 🧪 **Experiment 1:** Zie [exp001_baseline_rottermaatje.md](./findings/exp001_baseline_rottermaatje.md) voor de volledige testresultaten en hallucinatie-analyse.

**21-01-2026**
Verder gedoken in het eerste experiment ([exp001](./findings/exp001_baseline_rottermaatje.md)), resultaat geanalyseerd en geconcludeerd dat we een grotere dataset nodig hebben met diverse topics en talen. 250 meer synthetische data gegenereerd met een verbeterde verdeling van data over verschillende topics.

**Taalbalans**
De verdeling is opvallend evenwichtig over alle 4 de doeltalen:

Arabisch: 27,5% (SFT) / 23,0% (DPO)
Engels: 26,8% (SFT) / 21,7% (DPO)
Nederlands: 24,2% (SFT) / 29,0% (DPO)
Pools: 21,5% (SFT) / 26,3% (DPO)

**Onderwerpsdiversiteit** 
Het model ziet nu een veel breder scala aan onderwerpen:

Slapen/Opvang: ~33% (Dominant, zoals verwacht bij dakloosheid)
Juridisch/ID: ~31% (Cruciaal voor BSN/registratie)
Voedsel/Inkomen/Politie: ~12-16% per stuk
Medisch/Verslaving/Hygiëne: Aanwezig maar minder frequent (~10% gecombineerd)

**Succes tegen Hallucinaties**
Frequentie van "Gevangenis/Cel" context:

SFT: Slechts 2,0% (6 voorkomens)
DPO: Slechts 0,7% (2 voorkomens)

**24-01-2026**
Tweede experiment uitgevoerd, verminderde hallucinaties ten opzichte van [exp001](./findings/exp001_baseline_rottermaatje.md). Aantal features toegevoegd:
- Short term memory door coversatiegeheugen toe te voegen, door middel van de history te updaten na elke response (result.all_messages())
- Toolcalling schijnt lastiger te zijn voor kleine parameter LLMs, vandaar dat ik een functie heb toegevoegd om RAG uit te voeren bij iedere response dat in de context wordt toegevoegd. Dit simuleerd als het ware een toolcall naar de vector database.

> 🧪 **Experiment 2:** Zie [exp002_instruct_rottermaatje.md](./findings/exp002_instruct_rottermaatje.md) voor de volledige vergelijking met exp001 en de verbeterde resultaten.

**25-01-2026**
Opschoning van project folder, verwijderen van testfuncties en onnodige bestanden. De markdown formatting van docs/ aangepast voor betere leesbaarheid. Daarnaast de README.md en chainlit.md bijgewerkt met de laatste informatie.

## Samenvatting

Dit project documenteert de ontwikkeling van RotterMaatje, een AI-chatbot die daklozen en vrijwilligers in Rotterdam ondersteunt bij het vinden van opvang, voedsel en medische hulp.

### Fase 1: Technische Setup (november–december 2025)
Het project startte met de initialisatie van een gestructureerde ontwikkelomgeving met uv package manager. Verschillende kleine LLM's werden getest op een RTX 3050 (4GB VRAM), waaronder Qwen3-4B, Qwen3-8B en DeepSeek-modellen. Uiteindelijk werd qwen3-4b-2507 gekozen vanwege de optimale balans tussen snelheid, meertaligheid en VRAM-gebruik.

### Fase 2: Agent Architectuur (december 2025)
Een hybride architectuur werd ontwikkeld met een Triage Agent voor veiligheidsclassificatie (gpt-oss-safeguard-20b) en een interactie-agent (Grok-4.1-fast). Er werd een kennisbank opgebouwd met geverifieerde data uit de Pauluskerk FAQ en de Algemene Plaatselijke Verordening (APV) van Rotterdam, opgeslagen in een pgvector database voor semantisch zoeken.

### Fase 3: Fine-Tuning (januari 2026)
Het qwen3-4b-instruct model werd getraind via Supervised Fine-Tuning (SFT) en Direct Preference Optimization (DPO) in Google Colab, vanwege hardware-beperkingen. De eerste fine-tuning run ([exp001](./findings/exp001_baseline_rottermaatje.md)) toonde hallucinaties door overfit op gevangeniscontext. Dit werd opgelost in [exp002](./findings/exp002_instruct_rottermaatje.md) door het datavolume te vervijfvoudigen (~300 SFT + 300 DPO voorbeelden) met evenwichtige taalverdeling (Nederlands, Engels, Pools, Arabisch).

### Fase 4: Productie-features (januari 2026)
Kernfuncties werden geïmplementeerd: bestandupload voor intakeformulieren, vertalingsfunctie voor meertalige ondersteuning, privacy-guardrails (geen BSN/naam opslag), en conversatiegeheugen voor context-aware interacties. Een [testcasus met een alcoholverslavingssituatie](./findings/test_casus_intakeformulier.md) bewees de effectiviteit van de chatbot bij complexe hulpvragen.

### Conclusie
Het project demonstreert een iteratieve, data-gedreven aanpak waarbij hallucinaties werden opgelost door datadiversiteit, en waarbij een hybride lokaal/cloud architectuur een kostenefficiënte en veilige hulpverlening kan bevorderen.
