# Testcasus: Intakeformulier Analyse

## Context

Om de bestandupload functionaliteit te testen, is een intakeformulier gegenereerd met Google Gemini Pro 3 en geüpload via de frontend. Dit document beschrijft de chatbot-interactie en analyseert de effectiviteit van de hulpverlening door data-extractie te koppelen aan concrete acties.

**Databron:** `Jack/data/intake_formulier_casus.txt`

---

## Casus: "Jonathan" (GHB & Dakloosheid)

### Fase 1: Veiligheids- & Risicoanalyse

Het systeem voert eerst een automatische controle uit om de urgentie en de aard van de hulpvraag te bepalen.

| Kenmerk | Status |
|---------|--------|
| **Categorie** | 🏥 Medische hulp / Zorg |
| **Taal** | Nederlands (NL) |
| **Spoedgeval** | ✅ Geen direct levensgevaar (Stabiel maar acuut) |
| **Analyse** | De gebruiker meldt een zware GHB-verslaving. Dit is een medisch risico (kans op insulten/delier). De focus ligt op veilige detox en opvang, niet op acute reanimatie. |

---

### Fase 2: Strategie Hulpverlening (RotterMaatje)

De AI neemt de rol aan van een lokale gids, specifiek gericht op de situatie in Rotterdam.

> **Privacywaarschuwing:** Persoonlijke gegevens (Naam, BSN) worden niet opgeslagen in het systeem om de anonimiteit en veiligheid van de gebruiker te waarborgen.

> **Medische Waarschuwing:** Directe waarschuwing tegen "cold turkey" stoppen met GHB vanwege het hoge risico op medische complicaties.

---

### Fase 3: Gestructureerde Reactie RotterMaatje

#### Directe Actiepunten

| Actie | Details |
|-------|---------|
| **Verslavingshulp** | Ga direct naar Straatzorg Rotterdam |
| **Adres** | Mathenesserlaan 433 |
| **Telefoon** | 010-3188188 |
| **Doel** | Medische verwijzing naar een detox-kliniek |

**Aanvullende adviezen:**
- **Nachtopvang:** Houd rekening met de regiobinding. Ben je ingeschreven in Rotterdam? Zo niet, dan kan de opvang je doorverwijzen naar je eigen gemeente.
- **Geen Huisarts?** Geen probleem. Straatzorg fungeert als medisch aanspreekpunt voor mensen op straat.

#### Verduidelijkende Vragen

De chatbot vraagt proactief door voor extra informatie:
1. Kom je uit de regio Rotterdam en waar sta je momenteel ingeschreven?
2. Heb je specifieke zorgbehoeften (bijv. partner, huisdier of fysieke beperkingen)?
3. Zijn er naast de verslaving andere medische problemen bekend?

---

### Fase 4: Crisis-vangnet & Hulplijnen

De interactie sluit af met een overzicht van noodnummers en gespecialiseerde instanties in Nederland.

| Instantie | Contactgegevens |
|-----------|-----------------|
| **Spoed (Levensgevaar)** | 112 |
| **Zelfmoordpreventie** | 113 (of 0800-0113) |
| **Verslavingszorg (Jellinek)** | 088-505 1220 |
| **Pauluskerk Rotterdam** | 010-411 81 32 |
| **Veilig Thuis (Geweld/Misbruik)** | 0800-2000 |

---

## Effectiviteitsanalyse

### ✅ Sterke Punten

| Aspect | Beoordeling |
|--------|-------------|
| **Medische Prioriteit** | De AI herkent correct dat GHB-onthouding levensgevaarlijk is en adviseert medische begeleiding in plaats van alleen een bed. |
| **Lokale Relevantie** | Er wordt verwezen naar specifieke Rotterdamse locaties (Mathenesserlaan) die aansluiten bij de hulpvraag rondom de Pauluskerk. |
| **Stapsgewijze Hulp** | In plaats van een muur van tekst, krijgt de gebruiker een duidelijk pad: eerst medische stabilisatie, dan opvang. |
| **Proactieve Uitvraag** | De chatbot vraagt door naar inschrijfregio, zorgbehoeften en medische problemen. |
| **Dataverificatie** | Locaties zijn afkomstig uit de interne kennisbank (Pauluskerk FAQ) en geverifieerd via VectorDB queries. |

### ⚠️ Aandachtspunten

| Aspect | Observatie |
|--------|------------|
| **Financiële informatie** | De chatbot heeft niet de financiële situatie aangekaart (premie-achterstand). |
| **Uitkeringsadvies** | Geen sturing voor de aanvraag voor Wajong of Bijstandsuitkering. |
| **Oorzaak** | Beperkte data in de kennisbank over financiële hulpverlening. |

---

## Technische Configuratie

| Component | Model/Tool |
|-----------|------------|
| **Triage Agent** | `gpt-oss-safeguard-20b` |
| **Conversatie Agent** | `x-ai/grok-4.1-fast` |
| **Kennisbank** | pgvector + Supabase |
| **Embeddings** | `openai/text-embedding-3-small` |

**Motivatie voor Grok-4.1-fast:** Snelheid voor iteratief experimenteren en aantrekkelijke API-kosten.

---

## Conclusie

De effectiviteit van de chatbot is bewezen als zeer gewenst voor complexe hulpvragen. De combinatie van een veiligheidsgerichte triage (Safeguard-20b) en een snelle interactie-agent (Grok-4.1-fast) biedt een robuust systeem dat zowel veilig als kostenefficiënt is. De kennisbank kan worden uitgebreid met financiële hulpverleningsdata om de dekking te verbeteren.