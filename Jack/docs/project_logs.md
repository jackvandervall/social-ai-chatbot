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
Verder gewerkt aan de fine-tuning code, ik heb gekozen voor parameter-efficient fine-tuning (PEFT) met LoRA (Low-Rank Adaptation) in plaats van volledige fine-tuning, zodat het mogelijk is om het model te trainen op een consumer hardware zoals een RTX 3060 6GB. Persoonlijk heb ik een GTX 3050 4GB, dus ik kan geen volledige fine-tuning doen of moet overstappen op Qwen2.5-3B-Instruct, ~3.2 GB, goede kwaliteit met multilingual support. Waarschijnlijk ga ik kijken naar een betere LLM die ik kan trainen in een cloud-omgeving zoals Google Colab of van Hogeschool Rotterdam Datalab.

Voor de Reinforcement Learning (RL) heb ik gekozen voor Direct Preference Optimization (DPO), omdat het stabieler en efficiënter is dan traditionele RLHF, directe optimalisatie van gebruikersvoorkeuren mogelijk maakt zonder complex reward model, en naadloos integreert met Unsloth voor snelle training op hardware met beperkt VRAM.

**17-01-2026**
Aanpassingen gedaan aan de agent, namelijk een vertalingsfunctie op het advies van de chatbot, zodat de vrijwilligers de adviezen in de taal van de dakloze kunnen laten lezen. Daarnaast een gebruikersinstructie in de 'Leesmij' knop op de frontend. De system prompts zijn nu dynamisch en worden aangepast op basis van de type gebruiker, 'volunteer' of 'direct'.

Voor veiligheidsredenen heb ik guardrails gemaakt zodat de chatbot nooit naar een volledige naam, BSN, of gevoelige persoonsgegevens zal vragen. Daarnaast zijn er overige instanties bijgevoegd aan de safety disclaimers van de triage agent, inclusief links naar de instanties voor real-time verificatie. 

Tot slot heb ik relevante gegevens uit de Algemeen Plaatselijke Verordening (APV) van de gemeente Rotterdam, gehaald en in de vector database toegevoegd. Hier staan regels over openbare orde en veiligheid, verkeerszaken en horeca-aangelegenheden. Hier is een algemene script voor gemaakt zodat ik van meerdere bronnen soortgelijke informatie kan importeren en in de vector database toevoegen. 

Hoe ik de data structureer voor de vector database, is door de html code te parseren door een LLM (Google Gemini Pro 3), met de volgende prompt:

Extract alle informatie die toepasselijk is op dak- en thuisloze personen.

Verander het daarna in een vraag en antwoord format:

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

Met deze data kan de chatbot door middel van de pgvector tool gemakkelijk de juiste informatie vinden, door de implementatie van een vector database is dit erg schaalbaar.

**18-01-2026**
Om de triage van de gebruikers input classificatie te versnellen en kostenefficiënter te maken heb ik ervoor gekozen om in llm.py de gebruikte llm op te splitten. Voor classificatie heb ik gekozen voor een API call naar Openrouter met gpt-oss-safeguard-20b, het een safety reasoning model van OpenAI, gebouwd op basis van gpt-oss-20b. Dit is een Mixture-of-Experts (MoE) model met lower latency (goed voor triage), gemaakt voor veiligheidstaken zoals content classification, LLM filtering, en trust & safety labeling. Met deze setup worden de juiste safety disclaimers gegeven en kan er tijdens een noodgeval de chat stopgezet worden, om de gebruiker direct op de hoogte te stellen van de ernst van de situatie zodat hulpdiensten z.s.m. ingeschakeld kunnen worden. (Voorbeeld: "De cliënt voelt pijn op de borst", wat kan duiden op een hartaanval)

Naast het aanpassen van de triage agent, heb ik ook de bestandupload functionaliteit geïmplementeerd, hierdoor kunnen vrijwilligers intakeformulieren laten invullen en versturen voor de juiste verwijzing naar hulpinstanties. Ik heb dit uitgetest door een intakeformulier te genereren met Google Gemini Pro 3, en deze te uploaden via de frontend. Hierdoor kan de chatbot de juiste informatie uit het formulier halen en de vrijwilliger de juiste adviezen geven. De interactie ging als volgt:

Hieronder is de chatbot-interactie omgezet naar een gestructureerd Markdown-format. Dit overzicht toont de effectiviteit van de hulpverlening door data-extractie te koppelen aan concrete acties.

#Hieronder is de interactie vertaald en omgezet naar een gestructureerd overzicht in Markdown. Dit laat zien hoe effectief de AI schakelt tussen veiligheidscontrole, directe hulpverlening en lokale actiepunten.

---

## **Interactieoverzicht: Casus "Jonathan" (GHB & Dakloosheid)**

### **Fase 1: Veiligheids- & Risicoanalyse**

Het systeem voert eerst een automatische controle uit om de urgentie en de aard van de hulpvraag te bepalen.

| Kenmerk | Status |
| --- | --- |
| **Categorie** | 🏥 Medische hulp / Zorg |
| **Taal** | Nederlands (NL) |
| **Spoedgeval** | ✅ **Geen direct levensgevaar** (Stabiel maar acuut) |
| **Analyse** | De gebruiker meldt een zware GHB-verslaving. Dit is een medisch risico (kans op insulten/delier). De focus ligt op veilige detox en opvang, niet op acute reanimatie. |

---

### **Fase 2: Strategie Hulpverlening (RotterMaatje)**

De AI neemt de rol aan van een lokale gids, specifiek gericht op de situatie in Rotterdam.

> **Privacywaarschuwing:** Persoonlijke gegevens (Naam, BSN) worden niet opgeslagen in het systeem om de anonimiteit en veiligheid van de gebruiker te waarborgen.
> **Medische Waarschuwing:** Directe waarschuwing tegen "cold turkey" stoppen met GHB vanwege het hoge risico op medische complicaties.

---

### **Fase 3: Gestructureerde Reactie "RotterMaatje"**

### **Directe Actiepunten**

* **Verslavingshulp:** Ga direct naar **Straatzorg Rotterdam**.
* **Adres:** Mathenesserlaan 433
* **Telefoon:** 010-3188188
* *Doel:* Zij verzorgen de medische verwijzing naar een detox-kliniek.


* **Nachtopvang:** Houd rekening met de **regiobinding**. Ben je ingeschreven in Rotterdam? Zo niet, dan kan de opvang je doorverwijzen naar je eigen gemeente.
* **Geen Huisarts?** Geen probleem. Straatzorg fungeert als medisch aanspreekpunt voor mensen op straat.

### **Verduidelijkende Vragen voor Meer Hulp**

* Kom je uit de regio Rotterdam en waar sta je momenteel ingeschreven?
* Heb je specifieke zorgbehoeften (bijv. partner, huisdier of fysieke beperkingen)?
* Zijn er naast de verslaving andere medische problemen bekend?

---

### **Fase 4: Crisis-vangnet & Hulplijnen**

De interactie sluit af met een overzicht van noodnummers en gespecialiseerde instanties in Nederland.

| Instantie | Contactgegevens |
| --- | --- |
| **Spoed (Levensgevaar)** | 112 |
| **Zelfmoordpreventie** | 113 (of 0800-0113) |
| **Verslavingszorg (Jellinek)** | 088-505 1220 |
| **Pauluskerk Rotterdam** | 010-411 81 32 |
| **Veilig Thuis (Geweld/Misbruik)** | 0800-2000 |

---

### **Effectiviteit van deze Aanpak**

* **Medische Prioriteit:** De AI herkent correct dat GHB-onthouding levensgevaarlijk is en adviseert medische begeleiding in plaats van alleen een bed.
* **Lokale Relevantie:** Er wordt verwezen naar specifieke Rotterdamse locaties (Mathenesserlaan) die aansluiten bij de hulpvraag rondom de Pauluskerk.
* **Stapsgewijze Hulp:** In plaats van een muur van tekst, krijgt de gebruiker een duidelijk pad: eerst medische stabilisatie, dan opvang.

De effecitivteit is bewezen als zeer gewenst, door gebruik te maken van gpt-oss-safeguard-20b voor triage en x-ai/grok-4.1-fast voor de chatbot en toolcalls. x-ai/grok-4.1-fast vanwege de snelheid voor iteratief experimenteren en aantrekkelijke API-kosten. De locaties van de instanties zijn afkomstig uit de interne kennisbank, onder andere de faq geleverd door de Pauluskerk, dit is door de chatbot zelf geverifieerde data, door middel van vectordb queries. De chatbot stopt niet alleen bij het leveren van informatie, maar vraagt ook door voor extra informatie, zoals de inschrijfregio van de cliënt, overige zorgbehoeften en andere medische problemen. De chatbot kwam wellicht te kort bij de hoeveelheid informatie die is gegeven, het heeft bijvoorbeeld niet de financiële informatie aangekaart (premie-achterstand), maar hier is in de kennisbank ook weinig data over te vinden. Geen sturing voor de aanvraag voor Wajong of Bijstandsuitkering. (Bron: Jack\data\intake_formulier_casus.txt)

**19-01-2026**
Vandaag heb ik data gegenereerd om het qwen3-4b-instruct model te fine-tunen. Om de data te generenen heb ik Deepseek V3.2 gebruikt voor data-generatie vanwege lage kosten en meertalige kracht. De data is gegenereerd op basis van reële interacties en topics vanuit de data in de interne kennisbank. Daarnaast is ook GPO reinforcement learning toegepast, waardoor de LLM ook leert om een foutieve toon en incorrecte data te vermijden. Zelfs met quentization kon ik het niet lokaal trainen, vanwege deze error:

>"ValueError: Some modules are dispatched on the CPU or the disk. Make sure you have enough GPU RAM to fit the quantized model."

Vandaar dat ik het via Google Colab heb gedaan. Hieronder de resultaten:

🧪 Testing fine-tuned model:

The attention mask is not set and cannot be inferred from input because pad token is same as eos token. As a consequence, you may observe unexpected behavior. Please pass your input's `attention_mask` to obtain reliable results.

📝 User: Ik ben dakloos en heb honger. Waar kan ik eten krijgen?...
🤖 RotterMaatje: Ik begrijp dat het moeilijk is als je net uit de gevangenis komt. Er zijn plaatsen in Rotterdam waar je kunt eten. Bij de Pauluskerk op Delftseplein 25, de Wassel-De Vries op 's Gravendijkwal 49 en de...
------------------------------------------------------------
📝 User: I see a homeless person on the street. What can I do to help...
🤖 RotterMaatje: Thank you for asking. Helping homeless individuals is important. You can support them by volunteering at Pauluskerk, donating to their cause, or reporting their presence to the municipality. If you ne...
------------------------------------------------------------
📝 User: أين يمكنني العثور على مأوى ليلي في روتردام؟...
🤖 RotterMaatje: مرحبًا! نعم، يمكنني مساعدتك. مأوى NAS المخصص للبالغين موجود في فيجرهافسترات 29-31 في روتردام. هل الشخص الذي تساعده من منطقة روتردام؟ هذا مهم لتأكيد إمكانية الوصول إلى المأوى....
------------------------------------------------------------
📝 User: Gdzie mogę znaleźć nocleg w Rotterdamie?...
🤖 RotterMaatje: Cześć! W Rotterdamie dostępne są różne pokoje noclegowe dla tych, którzy potrzebują mieszkania. Czy jesteś z regionu Rotterdamu lub zarejestrowałeś się w regionie ostatnio? To ważne dla dostępu do nie...
------------------------------------------------------------

Zoals te zien is uit de test output, geeft het model op empathische manier antwoord. Er is alleen een merkwaardig antwoord gegenereerd, waarin de LLM ervan uit lijkt te gaan dat de user uit de gevangenis komt, in tegenstelling tot de initiële prompt, waarbij de user dakloos is en honger heeft. Dit kan komen door de data die is gebruikt voor het fine-tunen, waarbij er ook data is gebruikt over mensen die uit de gevangenis komen, mogelijke overtraining heeft voor deze hallucinatie gezorgt. Het is belangrijk om diverse data te hebben voor het fine-tunen om deze bias te voorkomen.