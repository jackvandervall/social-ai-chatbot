## Verantwoording LLM Keuze

### Hardware Situatie

* **Laptop:** ASUS TUF Gaming A15 (FA506ICB).
* **GPU:** **NVIDIA GeForce RTX 3050** (4 GB VRAM).
* **De Bottleneck:** **4 GB VRAM is de harde grens.**
* Modellen < 4 GB: Draaien volledig op GPU (snel).
* Modellen > 4 GB (zoals 7B/8B): Moeten uitwijken naar systeem-RAM. Dit maakt ze onwerkbaar traag voor realtime gebruik.

### Overwogen Alternatieven

* **Gemma 3 4B Instruct (Q4):** Past net (~3.0 GB). Goede balans, maar niet mijn keuze.
* **Llama 3.2 3B Instruct (Q6/Q8):** Zeer snel en zuinig (~2.5 GB), maar mist diepgang voor complex werk.
* **Qwen2.5-Coder 3B:** Uitstekend voor code, minder sterk in algemene tekst.
* **Phi-3.5 Mini / Qwen 2.5 7B:** Te zwaar. Phi zit op het randje van crashen; Qwen 7B is te traag door RAM-offloading.

### Definitieve Keuze: qwen3-4b-2507

Ik heb uiteindelijk gekozen voor **qwen3-4b-2507**.

* **Reden:** Dit model biedt de hoogste intelligentie die nog *volledig* binnen de 4 GB VRAM van de RTX 3050 past.
* **Prestaties:** Het is nieuwer en efficiënter dan de Gemma- en Llama-varianten en biedt een betere trade-off tussen snelheid en redeneervermogen dan de oudere Qwen 2.5-serie.

### Iteratieve Productie & Modelkeuze

Voor de eventuele productie van RotterMaatje is een model nodig met een optimale balans tussen **redeneervermogen (reasoning)**, **tool-calling** en **kostenefficiëntie**.

* **Voorkeur voor Productie:** **DeepSeek-V3.2**. Dit model biedt superieure prestaties voor een lage prijs, maar is momenteel **ongeschikt** vanwege strikte privacy- en veiligheidsrisico's.
* **Dataopslag:** Gegevens worden opgeslagen op Chinese servers.
* **Juridisch risico:** Onder de Chinese wetgeving kan de overheid toegang eisen tot deze data, wat strijdig is met de AVG/GDPR-normen voor lokale projecten.
* **Overheidsbeleid:** Sinds 2025 geldt er binnen diverse Europese en Amerikaanse overheidsinstanties een verbod op het gebruik van DeepSeek-API's voor gevoelige data.


* **Testfase (Prompts & Input):** Voor het snel en goedkoop valideren van prompts en inputdata gebruik ik **x-ai/grok-4.1-fast**.
* **Voordelen:** Lage latency en geoptimaliseerd voor agentic workflows (tool-calling), waardoor het een efficiënt alternatief is tijdens de ontwikkelingsfase.
Hier is de beknopte en zakelijke versie van de verantwoording, inclusief de toevoeging van de triage-component en de resultaten van de casus.

### Triage & Veiligheid

Voor de kritieke triagefase is gekozen voor **openai/gpt-oss-safeguard-20b**.

* **Rol in Productie:** Dit model fungeert als "gatekeeper" voor de triage. Het is specifiek getraind om input te toetsen aan strikte veiligheidspolicies en biedt volledige *chain-of-thought* transparantie bij beslissingen.
* **Architectuur:** Door de combinatie van **Safeguard-20b** (veiligheid/triage) en **Grok-4.1-fast** (interactie/tools) ontstaat een robuust systeem dat zowel veilig als kostenefficiënt is voor grootschalig gebruik.

### Datavalidatie & Kennisbank

De betrouwbaarheid van de chatbot wordt gewaarborgd door een gesloten kennissysteem:

* **Bron:** De interne kennisbank bevat geverifieerde data, zoals de FAQ van de Pauluskerk en Algemene Plaatselijke Verordening (APV) van de Gemeente Rotterdam.
* **Techniek:** Door gebruik van een **VectorDB** (RAG) voert de chatbot realtime queries uit om informatie te verifiëren voordat deze wordt gepresenteerd.
* **Interactie:** De chatbot is geprogrammeerd op proactieve uitvraag. Naast informatievoorziening vraagt het systeem gericht door naar de inschrijfregio, zorgbehoeften en medische achtergrond van de cliënt.
