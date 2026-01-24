## **Interactieoverzicht: Casus "Jonathan" (GHB & Dakloosheid)**

We hebben bestandupload functionaliteit geïmplementeerd, hierdoor kunnen vrijwilligers intakeformulieren invullen en versturen voor de juiste verwijzing naar hulpinstanties. We hebben dit uitgetest door een intakeformulier te genereren met de LLM Google Gemini Pro 3, en deze te uploaden via de frontend. Hierdoor kan de chatbot de juiste informatie uit het formulier halen en de vrijwilliger van de juiste adviezen voorzien.


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