# Modelconfiguratie – RotterMaatje

Dit document beschrijft welke AI-modelinstellingen zijn gebruikt tijdens
het testen en kiezen van het model voor het RotterMaatje-project.
Het doel van dit document is om inzichtelijk en reproduceerbaar te maken
hoe het model is gebruikt.

---

## 1. Modelinformatie

- **Modelnaam:** Qwen 3-4B Instruct (2507)
- **Modeltype:** Instruct
- **Modelprovider:** Qwen
- **Beschrijving:**  
  Qwen 3-4B is een instructiemodel dat goed kan omgaan met het opvolgen
  van opdrachten. Het model is geschikt voor meertalige taken en geeft
  relatief stabiele en consistente antwoorden. Dit maakt het model passend
  voor ondersteuning van vrijwilligers.

---

## 2. Backend & runtime-omgeving

- **Backend:** LM Studio (lokale OpenAI-compatible LLM-server)
- **Server type:** OpenAI-compatible local server
- **Base URL:** http://localhost:1234/v1
- **Platform:** macOS (Apple Silicon)
- **Gebruik:**  
  Het model wordt lokaal gedraaid om privacy te waarborgen, kosten te
  beperken en volledige controle te houden over modelgedrag tijdens tests.

---

## 3. Sampling- en generatieparameters

De onderstaande parameters zijn ingesteld via de LM Studio-interface:

- **Temperature:** 0.7  
- **Top-p (nucleus sampling):** 0.8  
- **Top-k:** 20  
- **Min-p:** 0  
- **Repeat penalty:** Uitgeschakeld  

Deze instellingen zorgen voor een balans tussen duidelijke antwoorden
en het voorkomen van te creatieve of onbetrouwbare output.

---

## 4. Contextlengte

- **Contextlengte (actief tijdens tests):** 4096 tokens  
- **Maximale contextlengte van het model (theoretisch):** 262.144 tokens  

**Toelichting:**  
Hoewel het model technisch een zeer lange context ondersteunt, is in dit
project gekozen voor een contextlengte van 4096 tokens. Dit past beter
bij lokaal gebruik en de standaardinstellingen van LM Studio.

---

## 5. System prompt

- **System prompt versie:** v1.0  
- **Doelgroep:** vrijwilligers en medewerkers van Team Aandacht & Welkom
  (Pauluskerk Rotterdam)
