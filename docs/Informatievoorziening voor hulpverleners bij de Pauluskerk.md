<div align="center">

# INFORMATIEVERZIENING VOOR HULPVERLENERS BIJ DE PAULUSKERK

**Brendan van der Sman 1016636**  
**Najah Khalifa: 1076514**  
**Jack van der Vall: 1081981**  
**Celine Scova Righini 1077277**

**Datum: 25/01/2026**

</div>

---

# Abstract

Dit onderzoek richtte zich op de vraag in hoeverre de AI-chatbot RotterMaatje vrijwilligers van de Pauluskerk Rotterdam kon ondersteunen bij de groeiende stroom hulpvragen van dak- en thuisloze. Door de stijgende dakloosheid nam de werkdruk toe, waardoor behoefte ontstond aan een systeem dat veelgestelde vragen snel en meertalig kon beantwoorden. Hiervoor hebben wij een technisch onderzoek uitgevoerd waarbij het lokale taalmodel Qwen3-4B-Instruct werd geoptimaliseerd door middel van Retrieval-Augmented Generation (RAG), Supervised Fine-Tuning (SFT) en Direct Preference Optimization (DPO). De chatbot werd in twee iteraties getest op meertaligheid en de nauwkeurigheid van de informatievoorziening op B1-taalniveau.

De resultaten toonden aan dat de inzet van een grotere dataset en DPO-training hallucinaties kan elimineren en dat het model feitelijke vragen over opvang en zorg juist kon beantwoorden in vier talen. Hoewel het model technische beperkingen vertoonde bij complexe taken zoals tool-calling, werd geconcludeerd dat RotterMaatje de informatieve druk op vrijwilligers kan verlagen. De inzet van een lokaal model waarborgde bovendien de privacy van kwetsbare bezoekers. Het onderzoek impliceert dat de chatbot een waardevolle assistent kan zijn, als het wordt ingezet als aanvulling en niet als vervanging van het essentiële menselijke contact binnen de Pauluskerk.

# Inhoudsopgave

- [Abstract](#abstract)
- [Inhoudsopgave](#inhoudsopgave)
- [Inleiding](#inleiding)
- [Probleemstelling en vraagstelling](#probleemstelling-en-vraagstelling)
	- [Centrale onderzoeksvraag](#centrale-onderzoeksvraag)
	- [Deelvragen](#deelvragen)
	- [Hypothese](#hypothese)
- [Methode](#methode)
- [Resultaten en Analyse](#resultaten-en-analyse)
	- [Uitgevoerde tests](#uitgevoerde-tests)
		- [1. Hardware Validatie en Training-setup](#1-hardware-validatie-en-training-setup)
		- [2. Iteratieve Model Tests (Exp001 vs. Exp002)](#2-iteratieve-model-tests-exp001-vs-exp002)
	- [Analyse en visualisatie](#analyse-en-visualisatie)
		- [Datadiversiteit en Onderwerpsverdeling](#datadiversiteit-en-onderwerpsverdeling)
		- [Analyse van Hallucinaties](#analyse-van-hallucinaties)
		- [Meertaligheid en Toon](#meertaligheid-en-toon)
- [Beantwoording](#beantwoording)
	- [Dekking van de Hulpvragen](#dekking-van-de-hulpvragen)
	- [Kwaliteit, Meertaligheid & Responsible AI](#kwaliteit-meertaligheid--responsible-ai)
	- [Verifieerbaarheid resultaten](#verifieerbaarheid-resultaten)
- [Discussie](#discussie)
	- [5.1 Methodologische beperkingen en blinde vlekken](#51-methodologische-beperkingen-en-blinde-vlekken)
	- [5.2 Linguïstische en Systematische beperkingen](#52-linguistische-en-systematische-beperkingen)
	- [5.3 Lokale AI en Veiligheid](#53-lokale-ai-en-veiligheid)
	- [5.4 Conclusie](#54-conclusie)
- [Conclusie](#conclusie)
	- [6.1 Samenvatting en bevindingen](#61-samenvatting-en-bevindingen)
	- [6.2 Beantwoording van de onderzoeksvragen](#62-beantwoording-van-de-onderzoeksvragen)
	- [6.3 Beperkingen](#63-beperkingen)
	- [6.4 Implicaties en suggesties](#64-implicaties-en-suggesties)
- [Literatuurlijst](#literatuurlijst)

# Inleiding

In Nederland is dak- en thuisloosheid een groeiend maatschappelijk probleem (Zien, n.d.). Volgens cijfers van het Centraal Bureau voor de Statistiek waren begin 2024 naar schatting ongeveer 33.000 mensen tussen de 18 en 65 jaar dakloos. Dit aantal is sinds 2022 met ruim 5.000 personen toegenomen (Centraal Bureau voor de Statistiek [CBS], 2025). Deze stijging zorgt voor toenemende druk op de maatschappelijke opvang en hulpverlening.

Dak- en thuisloze mensen zijn in sterke mate afhankelijk van maatschappelijke organisaties en vrijwilligers voor ondersteuning bij basisbehoeften, zoals opvang, zorg en voedsel (Planije et al., 2018). Organisaties geven aan dat opvanglocaties steeds vaker vol zitten en dat de werkdruk voor medewerkers en vrijwilligers de afgelopen jaren is toegenomen (Leger des Heils, z.d.). Hierdoor blijft er minder tijd over voor persoonlijke aandacht en begeleiding, terwijl deze juist belangrijk is voor deze kwetsbare doelgroep.

Ook in Rotterdam is deze problematiek zichtbaar (EenVandaag, 2025). De Rekenkamer Rotterdam concludeert dat de toegankelijkheid en continuïteit van ondersteuning onder druk staan door een groeiende doelgroep en beperkte capaciteit binnen de hulpverlening (Rekenkamer Rotterdam, 2023). Vrijwilligers en medewerkers moeten dagelijks veel bezoekers helpen met uiteenlopende, maar vaak terugkerende vragen over voorzieningen en ondersteuning.

Dit onderzoeksverslag richt zich op de praktijkcasus RotterMaatje bij de Pauluskerk Rotterdam. De Pauluskerk is een organisatie waar vrijwilligers dagelijks in contact staan met dak- en thuisloze bezoekers. In samenwerking met deze organisatie wordt onderzocht hoe een ondersteunende AI-chatbot, RotterMaatje, kan bijdragen aan het verlichten van de informatieve en logistieke druk op vrijwilligers. De chatbot is bedoeld als hulpmiddel om veelgestelde vragen toegankelijk, betrouwbaar en consistent te beantwoorden, zodat vrijwilligers meer ruimte houden voor persoonlijk contact en complexere hulpvragen.

**Organisatiecultuur**

De inzet van ondersteuning binnen de Pauluskerk Rotterdam kan niet los worden gezien van de organisatiecultuur. De Pauluskerk is een organisatie waarin het bieden van menselijke aandacht en betrokkenheid centraal staat (STICHTING DIACONAAL CENTRUM PAULUSKERK ROTTERDAM, 2021). Vrijwilligers en medewerkers werken vanuit een sociale en morele motivatie om kwetsbare mensen te ondersteunen, waarbij persoonlijk contact belangrijker is dan snelheid of standaardisering (STICHTING DIACONAAL CENTRUM PAULUSKERK ROTTERDAM, 2021).

Volgens de organisatietypologie van Mintzberg kan de Pauluskerk worden gekarakteriseerd als een missionaire organisatie. Dit type organisatie wordt gekenmerkt door een platte structuur en een sterke focus op gedeelde waarden en overtuigingen, in plaats van formele hiërarchie of efficiëntie als primair doel (Oldebijvank, 2025). Ook de Pauluskerk zelf benadrukt in haar missie en werkwijze het belang van mensgericht werken en nabijheid tot de doelgroep (Pauluskerk Rotterdam, n.d.).

**Demografische Diversiteit en Taalbarrières**

De groep dak- en thuisloze mensen in Nederland is niet alleen groot in omvang, maar ook divers samengesteld. Uit cijfers van CBS blijkt dat ongeveer de helft van deze groep een migratieachtergrond heeft (CBS, 2025). Van deze groep is 9% geboren in een ander Europees land en 37% buiten Europa. Daarnaast is 21% zelf in Nederland geboren, maar heeft één of beide ouders een migratieachtergrond. In de vier grootste steden, waaronder Rotterdam, ligt het aandeel dak- en thuisloze mensen met een migratieachtergrond hoger dan het landelijke gemiddelde (CBS, 2025).

Deze demografische kenmerken zijn relevant voor het ontwerp van RotterMaatje. Vrijwilligers van Team Aandacht & Welkom hebben dagelijks contact met bezoekers met diverse taalniveaus en achtergronden. Een chatbot die informatie eenvoudig, duidelijk en waar nodig meertalig aanbiedt, kan hen ondersteunen bij het toegankelijk uitleggen van informatie.

**Doelgroepanalyse vrijwilligers**

De vrijwilligers van Team Aandacht & Welkom van de Pauluskerk Rotterdam vormen het eerste aanspreekpunt voor bezoekers met diverse hulpvragen. Zij verwelkomen bezoekers, bieden een luisterend oor en beantwoorden praktische vragen over opvang, zorg en andere basisvoorzieningen (Pauluskerk Rotterdam, n.d.). Daarnaast hebben zij een signalerende rol: vrijwilligers moeten inschatten of een bezoeker geholpen is met basisinformatie of dat doorverwijzing naar een spreekuur, coördinator of specialist noodzakelijk is (zie bijlage A).

De bezoekersgroep van de Pauluskerk is divers en bestaat onder andere uit dak- en thuisloze mensen, Europese arbeidsmigranten, mensen zonder geldige verblijfspapieren, personen met een verslaving of psychiatrische problematiek, eenzame ouderen en jongeren met psychosociale problemen (Pauluskerk Rotterdam, n.d.).

In de dagelijkse praktijk ervaren vrijwilligers verschillende knelpunten bij het ondersteunen van bezoekers. Informatie over opvang, zorg en voorzieningen is vaak verspreid over meerdere bronnen, waardoor het lastig is om snel actuele en juiste informatie te vinden. Daarnaast maken taalverschillen, beperkte digitale vaardigheden en verschillende kwetsbaarheden bij bezoekers het voor vrijwilligers moeilijker om informatie goed te begrijpen en duidelijk uit te leggen (Planije et al., 2018; (Baay et al., 2015)). Deze knelpunten zijn bevestigd in feedback van medewerkers en vrijwilligers van de Pauluskerk, verzameld tijdens werksessies en overlegmomenten in het kader van het RotterMaatje-project (zie bijlage A).

**Ondersteuning van de doelgroep**

Het probleem laat zien dat vrijwilligers van Team Aandacht & Welkom dagelijks te maken krijgen met een groot aantal terugkerende hulpvragen. Het gaat hierbij vooral om vragen over basisvoorzieningen zoals onderdak, eten en drinken, maar ook om complexere onderwerpen zoals medische zorg, aanvragen van een BSN en vragen over juridische status (zie bijlage A en bijlage B).

Binnen dit project worden de vrijwilligers gezien als de directe gebruikers van RotterMaatje. De chatbot is bedoeld als ondersteunend hulpmiddel en niet als vervanging van menselijk contact. Vrijwilligers blijven verantwoordelijk voor het contact met bezoekers en voor het inschatten wanneer extra hulp of doorverwijzing nodig is. RotterMaatje ondersteunt hen door snel en betrouwbaar antwoorden te geven op veelgestelde vragen, eventueel in de moedertaal van de bezoeker, zonder dat hiervoor uitgebreide technische kennis nodig is (zie bijlage A).

Door vrijwilligers te ondersteunen met actuele en gecontroleerde informatie kan RotterMaatje bijdragen aan meer consistentie in de informatievoorziening. Hierdoor ontstaat meer ruimte voor vrijwilligers om aandacht te besteden aan persoonlijke gesprekken, signalering van problemen en het bieden van een gastvrije en veilige omgeving voor bezoekers (Planije et al., 2018).

**Stakeholderanalyse**

De belangen en rollen van de betrokkenen zijn geanalyseerd aan de hand van het door ons ontwikkelde Business Model Canvas (BMC) en het Value Proposition Canvas (VPC). Deze modellen maken inzichtelijk hoe RotterMaatje waarde toevoegt aan de organisatie en haar omgeving.

**Primaire stakeholders**

Vrijwilligers (Team Aandacht & Welkom): Zij zijn de directe gebruikers van de chatbot en staan centraal in ons Value Proposition Canvas (zie bijlage D). In de Customer Jobs van dit model zien we dat zij behoefte hebben aan zekerheid over de informatie die zij verstrekken en rust tijdens drukke momenten. RotterMaatje helpt hierbij als Pain Reliever door de zoektijd naar informatie te verminderen en stress te verlagen. De chatbot biedt ondersteuning zonder het menselijke contact over te nemen, wat een belangrijke Gain Creator is in ons model.

Dakloze personen in Rotterdam: Zij vormen het belangrijkste Customer Segment in ons BMC (zie bijlage c). Hoewel de vrijwilliger de chatbot bedient, is de uiteindelijke waarde voor de dakloze bezoeker het ontvangen van gelijke en betrouwbare informatie in de eigen taal. Zoals beschreven in de Value Proposition, helpt dit bij het verlagen van barrières voor kwetsbare groepen, zeker gezien de stijgende druk op de opvang (NL Times, 2025).

Pauluskerk: De Pauluskerk is in ons BMC zowel een Key Partner als de facilitator van de dagelijkse hulp. De chatbot ondersteunt de missie van de kerk door de werkdruk van vrijwilligers te verlichten en de kwaliteit van de hulpverlening te borgen. In het BMC valt dit onder de Key Activities: het verbeteren van de dagelijkse hulpverlening.

**Secundaire stakeholders**

Cegeka: Geïdentificeerd als de belangrijkste Key Supplier in ons BMC. Zij leveren de cruciale Key Resources (technische expertise en infrastructuur) die nodig zijn om de chatbot te ontwikkelen en te onderhouden. Hun belang ligt in de succesvolle implementatie en de ethische inrichting van het AI-systeem.

Andere daklozenopvangen in Rotterdam: Zij profiteren indirect van de Value Proposition van RotterMaatje. Door betere doorverwijzing en informatievoorziening bij de Pauluskerk, kan de ketendruk in heel Rotterdam worden verlaagd. Zij kunnen in de toekomst feedback leveren om de kennisbank verder te optimaliseren.

**Tertiaire stakeholders**

Gemeente Rotterdam/ Beleidsmakers: In ons BMC beschreven als Key Partner. De motivatie voor dit partnerschap is het laagdrempelig aanbieden van hulp om de zelfredzaamheid van kwetsbare burgers te vergroten, in lijn met het doel 'Kwetsbaren doen mee' uit de Voorjaarsnota 2025 (Gemeente Rotterdam, 2025). RotterMaatje ondersteunt deze ambitie door informatie over zorg en welzijn direct toegankelijk te maken voor dak- en thuisloze, wat bijdraagt aan de gemeentelijke doelstelling om ondersteuning effectiever en inclusiever in te richten.

Omwonenden van de Pauluskerk: Hoewel zij geen directe gebruikers zijn, hangt hun belang samen met de Value Proposition rondom informatie over openbare orde en voorzieningen. In het BMC draagt de chatbot bij aan een betere stroomlijning van bezoekers naar de juiste locaties (zoals douches of opvang), wat de leefbaarheid en veiligheid in de wijk ten goede komt (Hart van Nederland, 2024).

# Probleemstelling en vraagstelling

De Pauluskerk Rotterdam ondersteunt dak- en thuisloze met praktische hulp en informatievoorziening, waarbij Team Aandacht & Welkom (doelgroep 2) een rol heeft in het contact met bezoekers en het beantwoorden van vragen.

Uit de FAQ die is opgesteld in samenwerking met medewerkers en vrijwilligers van de Pauluskerk blijkt dat de hulpvragen vaak gaan over basisvoorzieningen, zoals opvang, eten en drinken, douchen, medische zorg, postadres/BSN/ID-documenten, inkomen/werk, verslaving, (terug)reizen en veiligheid/overlast (zie bijlage B).

Dak- en thuisloze kunnen moeite hebben om de juiste informatie te vinden door taalbarrières, problemen met het gebruik van digitale middelen en complexe regels (Hollimon et al., 2025). Dit sluit aan bij onderzoek waaruit blijkt dat lage taalvaardigheid het vinden en begrijpen van (online) informatie lastiger maakt, waardoor toegang tot diensten kan worden belemmerd (Baay et al., 2015).

Toegankelijkheid speelt een belangrijke rol binnen deze doelgroep. Uit onderzoek blijkt dat een deel van de doelgroep kenmerken heeft zoals een Licht Verstandelijke beperking (LVB)(Trimbos-insituut, 2024b). Uit stakeholderfeedback blijkt dat communicatie op taalniveau B1 het meest passend is voor deze doelgroep (zie bijlage A). Daarnaast wijzen eerdere studies erop dat ondersteunende middelen zoals audio (voorlezen) (Barai et al., 2021) en pictogrammen (Mbanda, 2021) helpend zijn voor laaggeletterden, analfabeten en mensen met LVB.

RotterMaatje wordt in de opdracht omschreven als een laagdrempelige, meertalige chatbot die dag en nacht beschikbaar is en in het gesprek kan inschatten wanneer iemand beter naar een medewerker moet worden doorverwezen. Tegelijk laten onderzoeken naar chatbots in de zorg zien dat dit soort systemen vaak nog niet streng genoeg is getest op veiligheid en werking. Vooral bij gevoelige onderwerpen (zoals medische of psychosociale problemen) kan het ontbreken van duidelijke regels voor wanneer en hoe je moet doorverwijzen ervoor zorgen dat het systeem een verkeerd of onveilig advies geeft (Car et al., 2020).

## Centrale onderzoeksvraag

Hoe kan RotterMaatje worden ontworpen en ingericht als ondersteunende AI-chatbot, gebaseerd op een taalmodel, voor team Aandacht & Welkom (doelgroep 2), zodat medewerkers en vrijwilligers veelgestelde vragen uit de praktijk snel, consistent en toegankelijk kunnen beantwoorden?

### Deelvragen

1. Met welke typen hulpvragen uit de bestaande FAQ krijgen medewerkers en vrijwilligers van team Aandacht & Welkom het vaakst te maken in de praktijk?
2. Welke functionele en technische eigenschappen moet RotterMaatje hebben om medewerkers en vrijwilligers van team Aandacht & Welkom effectief te ondersteunen?
3. Hoe kan de chatbot zo worden ontworpen dat deze aansluit bij verschillende taalniveaus en kwetsbaarheden van bezoekers, zonder de verantwoordelijkheid van medewerkers en vrijwilligers van team Aandacht & Welkom over te nemen?
4. Welke juridische en ethische aspecten zijn van belang bij het inzetten van een AI-chatbot als ondersteunend hulpmiddel voor medewerkers en vrijwilligers van team Aandacht & Welkom?

### Hypothese

De verwachting is dat RotterMaatje, wanneer deze wordt ontworpen met aandacht voor toegankelijkheid, duidelijke doorverwijsregels en betrouwbaar taalgebruik, medewerkers en vrijwilligers van Team Aandacht & Welkom ondersteunt bij het snel, consistent en toegankelijk beantwoorden van veelgestelde vragen, zonder het menselijke contact te vervangen.

# Methode

**Voorbereiding**

Om een geschikte keuze te maken tussen de verschillende Large Language Model (LLM) zijn de benodigde vereisten in kaart gebracht. Bijvoorbeeld gezien de diverse migratieachtergronden van dak- en thuisloze personen en de vrijwilligers is het van groot belang dat het taalmodel meertalig is (CBS, 2025). Om het besluit te nemen van een geschikt LLM zijn er gedurende de ontwikkeling meerdere taalmodellen getest, waarbij rekening is gehouden met de verschillende hardware-vereisten.

De uitvoering is begonnen met het testen van verschillende LLM-modellen met behulp van LM Studio. LM Studio is een programma wat mogelijk maakt om lokaal LLM-modellen te testen op de laptop. Bij het kiezen van het eindmodel waren er eisen. Voorbeelden van deze eisen waren:

- **Meertaligheid:** Het model behoort te communiceren in meerdere talen. Talen zoals Nederlands, Engels, Pools en Arabisch zijn talen die veel voortkomen bij dak- en thuisloze personen dus is het cruciaal dat het model deze talen beheerst (CBS, 2025).
- **Gebruik van toegankelijke taal:** Het model moet rekening houden met eventuele laag geletterdheid van dak- en thuisloze personen en is gediend te antwoorden met B1 taalniveau. (Stichting Lezen en Schrijven, 2016)
- **Rolbewust antwoorden:** Het model moet op basis van de rol van de gebruiker (dak- en thuisloze/ vrijwilligers) een gepaste reacties kunnen teruggeven.
- **Veiligheid en juistheid:** Model mag geen verzonnen of gevaarlijke informatie overbrengen (European Union, 2024).

Na het beoordelen van meerdere modellen is er uiteindelijk gekozen voor het model Qwen3-4B-2507, omdat het meest geschikt bleek voor de groepseisen en het einddoel (Qwen Team, 2025).

**Data – Interne Kennisbank**

Om de chatbot te voorzien van actuele en feitelijke informatie over gemeentelijk beleid en de door vrijwilligers van de Pauluskerk aangeleverde veel gestelde vragen (FAQ's) is er een robuuste Retrieval-Augmented Generation (RAG) pipeline ontwikkeld. Deze pipeline heeft als doel ongestructureerde bronnen te transformeren naar een semantisch doorzoekbare database.

De database kan worden gezien als een interne kennisbank. Deze kennisbank bevat datasets met informatie over de veel gestelde vragen zoals opvang locaties, het vinden van voedsel en drinken, medische hulp, hulp bij wetgeving etc. De database is opgesteld uit een bestaand document met veel gestelde vragen die door de doelgroep is aangeleverd. Daarnaast is er gebruik gemaakt van webscraping eigenhandig geselecteerde websites. Deze selectie is gemaakt op basis van relevantie en betrouwbaarheid. Zo zijn de bronnen afkomstig van websites van officiële instanties (zoals de Gemeente Rotterdam) en recente nieuwsartikelen.

Om de veiligheid en betrouwbaarheid van de outputs te behouden is het aantal toegankelijke websites bewust beperkt. Door het limiteren van vrije toegang tot het internet wordt de kans om risicovolle, schadelijke of onjuiste informatie te genereren een aanzienlijk stuk verkleind. Om consistentie vol te houden, beantwoordt de chatbot veelgestelde vragen uitsluitend op basis van de feitelijke FAQ van de Pauluskerk.

**Afkomst databronnen en extractie**

De kennisbank wordt gevoed door drie primaire bronnen:

- **APV Rotterdam:** De Algemene Plaatselijke Verordening, verkregen via rotterdam.nl.
- **Pauluskerk FAQ:** Specifieke hulpinformatie en veel gestelde vragen.
- **Gemeentelijke Nieuwsberichten:** Actuele berichtgeving gedownload als HTML-bronnen.

Om de chatbot te voorzien van de actuele kennis, gebruiken we een pipeline die:

- **Bronherkenning** uitvoert: Automatisch onderscheid maakt tussen beleidstukken en algemene informatie (FAQ).
- **Metadata:** Trefwoorden en bron-URL's toevoegt aan elke entry, wat essentieel is voor bronvermelding in de antwoorden van de chatbot.
- **Vectorisatie beheren:** De data wordt via een VectorDB service naar een PostgreSQL database pusht, daarnaast worden er checks uitgevoerd om duplicaten te voorkomen.

**Uitvoering en technieken**

De uitvoering van het project is gericht op het maken, testen en evalueren van het gekozen LLM binnen de context van de Pauluskerk. Voor de conversie van ongestructureerde HTML naar machine leesbare data is er gebruik gemaakt van state of the art model: Gemini 3 Pro. Dit model is ingezet om de ruwe tekst te structureren in een JSON format, waarbij categorieën, doelgroepen en trefwoorden automatisch worden herkend om de context beter te begrijpen. Deze data is opgeslagen in de eerder benoemde kennisbank.

Het antwoordgedrag van de chatbot is gestuurd via een vaste system prompt die aan de hand van concrete instructies, gedrags- en veiligheidsregels vastlegt.

Voorbeelden van de gedrag- en veiligheidsinstructies omvatten onder ander:

- Communiceren op Taalniveau B1 (gevraagd vanuit de opdracht gever).
- De chatbot vraagt niet naar persoonsgegevens (rekening houdend met de privacywetgeving (AVG)).
- Adressen, telefoonnummers en gelijksoortige informatie worden uitsluitend beantwoord gebaseerd op de interne kennisbank.
- Output mag een maximale lengte van vijf zinnen zijn.
- Vermijden van verzonnen informatie.
- Geen medisch, juridisch of psychologisch advies geven.

Daarnaast is er een safety-guard ingebouwd waarbij de input van de gebruiker eerst wordt geclassificeerd in onderwerp, taal en urgentie zodat de gepaste reactie wordt gegeven. Zo heeft het model vroegtijdig herkent wanneer er risicovolle of gevoelige situaties worden besproken. Bij het ontvangen van complexe situaties of vragen wordt het model geïnstrueerd om door te verwijzen naar de hulpdiensten of medewerker van de Pauluskerk. Dit gebeurt bij bijzondere situaties waar er eventueel om advies gevraagd wordt of kwetsbare onderwerpen besproken worden zoals psychische klachten. Dit zorgt ervoor dat het model niet zelf gaat hallucineren.

Voor trainings- en evaluatiedata wordt er gebruik gemaakt van zowel een system prompt als test prompts. De uitgebreide system prompt bevat alle benodigde eisen voor het gedrag van het model. Voor de test prompts zijn er verschillende scenario's opgesteld, waarbij er in het geval van de Reinforcementlearning data, per scenario de gewenste output als referentie worden meegegeven. Hierdoor leert het model de gewenste reacties.

De uiteindelijke evaluatie beoordeelt of de output correct en veilig is, hierbij wordt gecontroleerd of het model kan herkennen wanneer een situatie wel of niet urgent is en zal hierbij toepasselijk reageren met eventuele waarschuwingen.

**Beperkingen**

De aanpak kent beperkingen. Zo is de omvang van de dataset beperkt en is de data samengesteld uit handmatig verzamelde, grotendeels ongestructureerde tekstbronnen (zoals het FAQ-document van de Pauluskerk, nieuws artikelen en publieke websites). Daarnaast is de beschikbare rekenkracht beperkt, omdat het gekozen Qwen3-4B-2507 model vrij compact is (Qwen Team, 2025). Dit heeft invloed op de complexiteit en flexibiliteit van de gegenereerde antwoorden.

De tweede belangrijke beperking betreft op het gebied van data actualiteit. Informatie zoals beleidsinformatie, openingstijden of regels veranderen in praktijk regelmatig. Hierdoor zal de data in de kennisbanken niet actueel blijven als deze niet geregeld wordt bijgewerkt. Hoewel de chatbot is ingericht om bij onzekerheid of onwetendheid geen details te verzinnen en in plaats hiervan de gebruiker door te verwijzen naar instanties of vrijwilligers, blijft het onderhouden van de kennisbank noodzakelijk om de veiligheid en betrouwbaarheid te waarborgen.

Daarnaast is het model afgestemd op de context van Rotterdam, specifiek rondom de Pauluskerk. Buiten deze context is het model niet getraind, waardoor de betrouwbaarheid van de antwoorden in andere gemeenten niet gewaarborgd is.

Gezien de beperkingen ligt de nadruk op het conceptueel ontwerp en het verkennen van de technische haalbaarheid.

**Reproduceerbaarheid methode**

De gebruikte methode is grotendeels reproduceerbaar op methodeniveau. Een andere onderzoeksgroep kan het proces herhalen door vergelijkbare ongestructureerde tekstbronnen te verzamelen en deze op dezelfde wijze te structureren, op te schonen en te vereenvoudigen voor gebruik binnen het taalmodel.

De keuzes voor data voorbereiding, zoals het verwijderen van dubbele informatie, thematische clustering (het groeperen van vergelijkbare onderwerpen binnen de data) en het aanpassen van het taalniveau zijn duidelijk beschreven. Ook het werken met prompts om het taalmodel rolbewust te laten antwoorden is reproduceerbaar naar andere projecten die een vergelijkbare context hebben.

De uitkomsten zijn echter niet volledig reproduceerbaar, aangezien deze afhankelijk zijn van de specifieke context, inhoud van de documenten en de samenstelling van het taalmodel. Door dit te benoemen en geen extreme uitspraken te maken over de prestaties of betrouwbaarheid, blijft de analyse transparant en eerlijk.

# Resultaten en Analyse

In dit hoofdstuk worden de resultaten gepresenteerd van de ontwikkeling en tests van de RotterMaatje-chatbot. Het onderzoek is uitgevoerd in twee iteraties: een eerste baseline-experiment (exp001) om de technische pijplijn te valideren, en een tweede experiment (exp002) gericht op kwaliteitsverbetering en hallucinatie-reductie.

## Uitgevoerde tests

Om de centrale onderzoeksvraag te beantwoorden, zijn er testen uitgevoerd op drie vlakken: technische haalbaarheid op consumentenhardware, functionele kwaliteit van de output en de effectiviteit van de toegepaste fine-tuning methoden (SFT en DPO).

### 1. Hardware Validatie en Training-setup

De eerste testfase richtte zich op de technische randvoorwaarden. De doelstelling was om vast te stellen of het finetunen van een taalmodel mogelijk is op de beschikbare hardware (laptop met NVIDIA RTX 3050, 4GB VRAM), wat relevant is voor de kostenefficiëntie van de oplossing.

- **Opzet:** Er is geprobeerd het basismodel Qwen3-4B lokaal te finetunen met behulp van 4-bit kwantisatie (QLoRA) en Unsloth-optimalisatie.
- **Resultaat:** Lokale training bleek technisch onhaalbaar. Ondanks optimalisaties overschreed het trainingsproces de VRAM-limiet, resulterend in een Out Of Memory (OOM) error (`ValueError: Some modules are dispatched on the CPU`).
- **Correctie:** De rekenintensieve training is verplaatst naar een cloud-omgeving (Google Colab met T4 GPU), terwijl het gebruik van de chatbot wel succesvol bleek op de lokale hardware.
- **Trainingsefficiëntie:** De DPO-training op de dataset van 300 voorbeelden duurde slechts 6 minuten en 17 seconden op een enkele NVIDIA T4 GPU.
- **Parameter-efficiëntie:** Dankzij de Unsloth-optimalisatie hoefde slechts 0,81% van de parameters (ca. 33 miljoen) te worden getraind, wat het proces haalbaar maakte binnen de beperkingen van Google Colab.

**Figuur 1**

*Trainingsnauwkeurigheid van het RotterMaatje-model tijdens Direct Preference Optimization (DPO)*

Noot. Deze figuur illustreert de nauwkeurigheid van de voorkeursselectie tijdens de DPO-trainingsfase. De waarden, variërend van .95 tot 1.00, duiden op de consistentie van het model bij het selecteren van het geprefereerde (empathische/feitelijke) antwoord ten opzichte van het afgewezen (ongepast/gehallucineerde) antwoord.

### 2. Iteratieve Model Tests (Exp001 vs. Exp002)

Na de technische validatie zijn twee inhoudelijke experimenten uitgevoerd om de antwoordkwaliteit te toetsen.

- **Experiment 1 (Baseline):** Hierbij is het model qwen3-4b-2507 gefinetuned op een kleine dataset (n=50 SFT / n=50 DPO). Het doel was het testen van de meertaligheid en de integratie van RAG-kennis.
- **Experiment 2 (Optimalisatie):** Op basis van de bevindingen uit Exp001 is overgestapt naar het model qwen3-4b-instruct. De dataset is opgeschaald naar ~300 voorbeelden per methode en de datadiversiteit is vergroot om overfitting te bestrijden (n=300 SFT / n=300 DPO).

De resultaten zijn geëvalueerd aan de hand van gestandaardiseerde prompts in vier talen (Nederlands, Engels, Pools, Arabisch) en beoordeeld op empathie, feitelijke juistheid en veiligheid.

## Analyse en visualisatie

Uit de vergelijking tussen de twee experimenten komen duidelijke patronen naar voren met betrekking tot datakwaliteit, hallucinaties en meertaligheid.

### Datadiversiteit en Onderwerpsverdeling

In het tweede experiment is gestuurd op een verdeling van onderwerpen die relevant zijn voor de doelgroep. Waar het eerste experiment een beperkte focus had, toont de dataset van exp002 een brede dekking van essentiële levensbehoeften.

Deze verbreding van data blijkt cruciaal voor de stabiliteit van het model. Door de dataset te vergroten van ~100 regels (Exp001) naar ~600 regels (Exp002), is het risico op bias significant afgenomen.

**Tabel 1**

*Verdeling van Onderwerpen in Trainingsdata voor Fine-Tuning en Direct Preference Optimization*

Noot. Deze tabel illustreert de onderwerpen die gebruikt worden in de trainingsset zijn o.a. geëxtraheerd uit de interne kennisbank met veelgestelde vragen (Pauluskerk, persoonlijke communicatie, oktober 2025) en de Algemene Plaatselijke Verordening Rotterdam (Gemeente Rotterdam, 2012).

### Analyse van Hallucinaties

Een belangrijk resultaat uit de analyse is het effect van een Small Sample Size op de betrouwbaarheid.

- **Probleem (Exp001):** In de baseline-test vertoonde het model ernstige overfitting. Bij de prompt "Ik heb honger" hallucineerde het model dat de gebruiker net uit de gevangenis kwam. Dit werd veroorzaakt doordat 2% van de kleine trainingsset over ex-gedetineerden ging, wat het model onterecht generaliseerde naar alle gebruikers.
- **Oplossing (Exp002):** Door de dataset te vergroten en de specifieke gevangenis-casus te "verdunnen" (tot <0.7% in de DPO-set), is deze hallucinatie volledig weg.

**Tabel 2**

*Vergelijking Testoutput Exp001 en Exp002*

| Testoutput | Exp001 | Exp002 |
| --- | --- | --- |
| Ik ben dakloos en heb honger. Waar kan ik eten krijgen? | Ik begrijp dat het moeilijk is als je net uit de gevangenis komt. Er zijn plaatsen in Rotterdam waar je kunt eten. Bij de Pauluskerk op Delftseplein 25, de Wassel-De Vries… | Ik begrijp dat het moeilijk is als je dakloos bent en honger voelt. Er zijn plekken waar je eten kunt krijgen. Bijvoorbeeld, bij de Pauluskerk op Mauritsweg 20... |

Noot. In dit experiment is aangetoond dat de overgang van qwen-4b-2507 op qwen3-4b-instruct en een meer diverse trainingstest kan leiden tot minder hallucinaties (gevangenis-bias) in de testoutput.

### Meertaligheid en Toon

De resultaten tonen aan dat de keuze voor qwen3-4b-instruct in combinatie met DPO (Direct Preference Optimization) effectief is voor het behouden van een consistente, empathische toon in meerdere talen. Het model schakelt correct tussen Nederlands, Engels, Arabisch en Pools zonder verlies van context of feitelijke juistheid (zoals adressen van de Pauluskerk of opvanglocaties).

**Tabel 3**

*Taalverdeling in Trainingsdata voor Fine-Tunen en Direct Preference Optimization*

| Taal | SFT Dataset (n=300) | DPO Dataset (n=300) | Gecombineerd (n=600) |
| --- | --- | --- | --- |
| Nederlands | 74 (24.7%) | 89 (29.7%) | 163 (27.2%) |
| Engels | 80 (26.7%) | 65 (21.7%) | 145 (24.2%) |
| Pools | 64 (21.3%) | 79 (26.3%) | 143 (23.8%) |
| Arabisch | 82 (27.3%) | 67 (22.3%) | 149 (24.8%) |
| Totaal | 300 (100%) | 300 (100%) | 600 (100%) |

Noot. Deze tabel toont aan werden uniform willekeurig geselecteerd (random.choice(LANGUAGES)) tijdens het genereren van synthetische gegevens, met als doel een gelijke verdeling van 25% per taal.

# Beantwoording

## Dekking van de Hulpvragen

De analyse van de FAQ en praktijkdata toont aan dat de chatbot niet 'alles' hoeft te weten, maar moet excelleren in specifieke domeinen. De technische inrichting is succesvol afgestemd op de vastgestelde verdeling:

- **Slapen & Opvang (~33%):** De dominante categorie.
- **Juridisch & ID (~31%):** Cruciaal voor BSN-registratie.
- **Basisbehoeften (~36%):** Voedsel, inkomen en medische zorg. Het model is specifiek getraind om op deze onderwerpen feitelijk accuraat te zijn, in plaats van algemene conversatie te voeren.
- **Beperking:** De huidige data zoals contactinformatie, locaties kan veranderen, de RAG zou hiervoor regelmatig op worden geüpdatet als er nieuwe informatie zou bijkomen.

**Tabel – Onderwerpsverdeling**

| Onderwerp | Percentage |
| --- | --- |
| Slapen/Opvang | ~33% (Dominant, zoals verwacht bij dakloosheid) |
| Juridisch/ID | ~31% (Cruciaal voor BSN/registratie) |
| Voedsel | ~12-16% |
| Inkomen | ~12-16% |
| Politie/APV | ~12-16% |
| Medisch/Verslaving/Hygiëne | ~10% gecombineerd |

## Kwaliteit, Meertaligheid & Responsible AI

De inzet van SFT (kennis) in combinatie met DPO (toon) zorgt voor verbeterde consistentie.

- **Meertalige Ondersteuning:** Het model schakelt met behoud van empathie tussen Nederlands, Engels, Arabisch en Pools. Hiermee wordt technisch voldaan aan de eis om aan te sluiten bij diverse taalniveaus.
- **Hallucinatie & Bias:** Exp001 toonde aan dat een kleine dataset leidt tot schadelijke vooroordelen, door datadiversificatie in Exp002 lijkt de hallucinatie te zijn verdwenen.
- **Noodzaak Human-in-the-loop:** Ondanks de verbeteringen blijft het model niet-deterministisch. Voor een verantwoorde inzet (Responsible AI) is menselijke validatie een harde vereiste en zou het alleen als hulpmiddel moeten worden ingezet, geen vervanging.

## Verifieerbaarheid resultaten

Om de resultaten van dit onderzoek controleerbaar te maken voor onafhankelijke partijen, zijn de volgende stappen ondernomen:

- **Methodologie:** De gebruikte technieken (Unsloth, QLoRA, DPO) en hyperparameters zijn vastgelegd. De exacte modelkeuze (qwen3-4b-instruct) is gedocumenteerd.
- **Data-structuur:** De structuur van de gebruikte datasets (.jsonl formaat met System/User/Assistant rollen) is beschikbaar in de repository.
- **Reproduceerbaarheids-opmerking:** De datasets zijn gegenereerd met behulp van externe LLM-API's (DeepSeek V3.2). Omdat deze modellen niet-deterministisch zijn, kan het opnieuw genereren van de data leiden tot lichte variaties in de trainingsvoorbeelden. Echter, het getrainde model zelf (in .gguf formaat) levert bij inferentie consistente resultaten op die overeenkomen met de gepresenteerde logs.

# Discussie

In dit hoofdstuk reflecteren we op de resultaten. Hoewel de technische vooruitgang tussen de twee experimenten aanzienlijk is, blijven er vragen bestaan over de inzet van AI in een kwetsbare context.

## 5.1 Methodologische beperkingen en blinde vlekken

De betrouwbaarheid van RotterMaatje kan niet enkel worden vastgesteld op basis van succesvolle testlogs. We moeten kijken naar wat het model niet ziet.

- **Falsificatie en Edge Cases:** Volgens Karl Popper (1959) is een theorie of model pas wetenschappelijk als deze falsificeerbaar is. In ons onderzoek zagen we dit terug in Exp001: de "gevangenis-hallucinatie" was een cruciaal moment van falsificatie. Hoewel Exp002 deze specifieke fout heeft opgelost, stelt Popper dat we nooit kunnen bewijzen dat een model altijd de waarheid spreekt, we hebben enkel nog niet de volgende fout gevonden. Voor de Pauluskerk betekent dit dat er altijd een risico blijft op unieke fouten in crisissituaties die niet in de trainingsdata voorkwamen.
- **De blinde vlek van datificatie:** Naast de logische grenzen van Popper, moeten we het ook hebben over een fundamentele blinde vlek die filosoof Miriam Rasch (2020) omschrijft als het gevaar van datificatie. Onze hele methode is nu gericht op een proces zonder frictie, een bezoeker stelt een vraag en krijgt direct een efficiënt, gladgestreken antwoord.
- Maar daar zit precies het probleem. De blinde vlek van dit project is de frictie die juist de kern vormt van het werk bij de Pauluskerk. Rasch (2020) waarschuwt dat er iets essentieels kapotgaat als je zorg reduceert tot alleen maar informatievoorziening. Een chatbot is een smooth operator die taal verwerkt, maar hij mist het menselijke, de ongemakkelijke stiltes en de fysieke aanwezigheid die nodig zijn om de echte hulpvraag goed te kunnen horen. Waar onze chatbot een technisch perfect antwoord zoekt, vraagt de praktijk vaak juist om de vertraging en het menselijke stukje dat onze chatbot niet kan leveren.

## 5.2 Linguïstische en Systematische beperkingen

Als we kijken naar hoe RotterMaatje met taal omgaat, stuiten we op de grenzen van de huidige AI-technologie.

- **Statistiek versus Universele Grammatica:** Noam Chomsky (2023) stelt dat LLM's zoals Qwen3 fundamenteel verschillen van menselijke intelligentie. Waar een mens beschikt over een aangeboren vermogen om logische verbanden te leggen, doet RotterMaatje een geavanceerde statistische gok. Het model begrijpt niet wat honger is, het weet alleen dat na het woord honger vaak het woord eten of Pauluskerk volgt. Dit verklaart de hallucinaties in Exp001: het model volgde een statistisch pad (gevangenis-context) dat logisch gezien nergens op sloeg.
- **Taalspelen en de Leefvorm:** Ludwig Wittgenstein (1953) stelde dat de betekenis van woorden voortkomt uit hun gebruik in een specifieke leefvorm het taalspel. De Pauluskerk heeft een heel eigen taalspel, gebaseerd op gastvrijheid en radicale aanwezigheid. Een chatbot die getraind is op datasets buiten deze specifieke context, kan de woorden wel gebruiken, maar mist de geest van het gesprek. Het risico bestaat dat de antwoorden van RotterMaatje te klinisch of bureaucratisch worden, waardoor ze niet aansluiten bij de missionaire cultuur van de organisatie.

## 5.3 Lokale AI en Veiligheid

Een belangrijk punt van discussie is de technische beperking van het 4B-model. We hebben gezien dat dit model moeite heeft met complexe toolcalling.

Opmerking: Er ontstaat een spanningsveld tussen privacy en intelligentie. Om de privacy van ongedocumenteerde bezoekers te waarborgen, is een lokaal model (zoals Qwen3-4B) essentieel. Echter, de beperkte logische capaciteit van zulke kleine modellen maakt ze gevoeliger voor fouten in de RAG-pipeline. De vraag voor de Pauluskerk is: is een minder slim maar veilig lokaal model te verkiezen boven een geniaal maar onveilig cloud-model?

## 5.4 Conclusie

De overgang naar een instruct-model en het gebruik van DPO (Direct Preference Optimization) heeft de veiligheid vergroot, maar een chatbot in de context van de Pauluskerk moet altijd een ondersteunend middel blijven. De menselijke vrijwilliger gaat nodig zijn om de output van de AI te vertalen naar de empathische werkelijkheid van de bezoeker.

# Conclusie

## 6.1 Samenvatting en bevindingen

Dit onderzoek toont aan dat een speciaal getrainde, lokale AI-chatbot een waardevolle ondersteuning kan bieden voor de vrijwilligers van de Pauluskerk Rotterdam. De transitie van de eerste experimentele fase (exp001) naar de geoptimaliseerde fase (exp002) laat zien dat de betrouwbaarheid toeneemt wanneer er gebruik wordt gemaakt van een grotere, meer diverse dataset.

Een belangrijke bevinding is dat een compact taalmodel (Qwen3-4B-Instruct) in staat is om complexe, meertalige informatie over basisvoorzieningen (zoals opvang, medische zorg en juridische hulp) kan vertalen naar een toegankelijk B1-taalniveau. Hoewel lokale training op consumentenhardware technisch beperkt bleek door VRAM-limitaties, is het uiteindelijke gebruik van de chatbot succesvol lokaal uitvoerbaar. Hiermee wordt voldaan aan de wens voor privacy.

## 6.2 Beantwoording van de onderzoeksvragen

Op basis van de resultaten kan de centrale onderzoeksvraag als volgt worden beantwoord:

RotterMaatje kan effectief worden ontworpen als ondersteunende AI-chatbot door een RAG-pipeline (Retrieval-Augmented Generation) te combineren met een specifiek op de Pauluskerk gefinetuned model. Door de inzet van Supervised Fine-Tuning (SFT) voor feitelijke kennis en DPO voor een empathische, veilige toon, kunnen vrijwilligers van Team Aandacht & Welkom snel en consistent vragen beantwoorden.

- **Eigenschappen:** Essentiële kenmerken zijn de meertaligheid (Nederlands, Engels, Poolse en Arabisch) en het vermogen om bij complexe casuïstiek direct door te verwijzen naar menselijke coördinatoren.
- **Toegankelijkheid:** Door strikte instructies in de system prompt en training op diverse scenario's zorgt de chatbot dat de last van het opzoeken van informatie wordt vermindert.
- **Ethiek:** De keuze voor een lokaal model en het elimineren van hallucinaties (zoals de gevangenis-bias) zorgt voor een veilige interactie met de doelgroep.

## 6.3 Beperkingen

Ondanks de positieve resultaten kent het onderzoek enkele beperkingen:

- **Tool-calling:** Het 4B-model vertoont moeite met het autonoom aanroepen van externe functies (tool-calling) binnen de kennisbank, wat een op maat gemaakte technische oplossing vereiste.
- **Actualiteit:** De betrouwbaarheid van RotterMaatje is verbonden aan de kwaliteit van de onderliggende dataset. Zodra data als openingstijden veranderd, moet de kennisbank handmatig worden bijgewerkt om foutieve informatie te voorkomen.
- **Hardware:** De beperkte rekenkracht op locatie maakt het draaien van grotere, potentieel intelligentere modellen (bijv. 7B of 14B) moeilijk, waardoor er een balans gezocht moet worden tussen snelheid en diepgang.

## 6.4 Implicaties en suggesties

De resultaten suggereren dat RotterMaatje de werkdruk bij de Pauluskerk kan verlagen en kan zorgen voor een eenheid in de beschikbare informatie. Voor de praktijk en vervolgonderzoek worden de volgende stappen aanbevolen:

- **Human-in-the-loop implementatie:** Introduceer de chatbot als een hulpmiddel voor vrijwilligers op een tablet of desktop, waarbij de vrijwilliger het antwoord altijd valideert voordat het met de bezoeker wordt gedeeld. De chatbot zou nooit als vervanging voor een vrijwilliger moeten dienen.
- **Dynamisch onderhoud:** Ontwikkel een gebruiksvriendelijk dashboard voor medewerkers van de Pauluskerk om de FAQ-kennisbank eenvoudig te actualiseren zonder technische tussenkomst.
- **Vervolgonderzoek naar multimodaliteit:** Onderzoek de toevoeging van audio-output (voorleesfunctie) of pictogrammen in de interface om de toegankelijkheid voor analfabeten en mensen met een licht verstandelijke beperking (LVB) verder te vergroten.
- **Opschaling:** Test of de ontwikkelde RAG-structuur overdraagbaar is naar andere hulporganisaties in Rotterdam om de ketendruk in de gehele stad te verlichten.

# Literatuurlijst

Baay, P., Buisman, M., Houtkoop, W., Stichting Lezen & Schrijven, & Expertisecentrum Beroepsonderwijs. (2015). *Laaggeletterden: achterblijvers in de digitale wereld? Vaardigheden van burgers en aanpassingen door overheden.* Stichting Lezen & Schrijven. https://www.lezenenschrijven.nl/sites/default/files/2020-09/Laaggeletterden-achterblijvers-in-de-digitale-wereld-web-ecbo.pdf

Barai, P., Leroy, G., & Ahmaed, A. (2021). *Comparative Evaluation of Text and Audio Simplification: A Methodological Replication Study.* https://arxiv.org/pdf/2508.15088

Car, L. T., Dhinagaran, D. A., Kyaw, B. M., Kowatsch, T., Joty, S., Theng, Y., & Atun, R. (2020). Conversational Agents in Health Care: Scoping Review and Conceptual Analysis. *pmc.ncbi.nlm.nih.gov.* https://doi.org/10.2196/17158

Centraal Bureau voor de Statistiek. (2025, January 28). 33 duizend mensen dakloos begin 2024. *Centraal Bureau Voor De Statistiek.* https://www.cbs.nl/nl-nl/nieuws/2025/05/33-duizend-mensen-dakloos-begin-2024

Chomsky, N., Roberts, I., & Watumull, J. (2023, 8 maart). The False Promise of ChatGPT. *The New York Times.*

EenVandaag. (2025, January 28). Ook in Rotterdam is te merken dat aantal daklozen stijgt: "Ze breken in bij tuinhuisjes om te overleven." *EenVandaag.* https://eenvandaag.avrotros.nl/artikelen/ook-in-rotterdam-is-te-merken-dat-aantal-daklozen-stijgt-ze-breken-in-bij-tuinhuisjes-om-te-overleven-154405

European Union. (2024). Artificial Intelligence Act (Regulation (EU) 2024/1689), Article 15: Accuracy, robustness and cybersecurity. Geraadpleegd op 25 januari 2026, van https://artificialintelligenceact.eu/article/15/

Gemeente Rotterdam. (n.d.). *Openbare orde.* https://www.rotterdam.nl/openbare-orde

Gemeente Rotterdam. (2025). *Voorjaarsnota 2025: Zorg, welzijn en wijkteams - Kwetsbaren doen mee.* https://www.watdoetdegemeente.rotterdam.nl/voorjaarsnota-2025/programmas/zorg-welzijn-en-wijkteams/doel-kwetsbaren-doen-mee/

Hart van Nederland. (2024, March 1). Omwonenden Pauluskerk ervaren overlast door daklozen. https://www.hartvannederland.nl/algemeen-nieuws/artikelen/omwonenden-pauluskerk-overlast-daklozen

Hollimon, L. A., Taylor, K. V., Fiegenbaum, R., Carrasco, M., Gomez, L. G., Chung, D., & Seixas, A. A. (2025). Redefining and solving the digital divide and exclusion to improve healthcare: going beyond access to include availability, adequacy, acceptability, and affordability. *Frontiers in Digital Health, 7*, 1508686. https://doi.org/10.3389/fdgth.2025.1508686

Leger des Heils. (n.d.). *Crisissituatie dak- en thuisloosheid.* https://www.legerdesheils.nl/artikel/crisissituatie-dak-en-thuisloosheid

Mbanda. (2021). *A scoping review of the use of visual aids in health education materials for persons with low-literacy levels.* https://repository.up.ac.za/server/api/core/bitstreams/53e89a6d-91c7-428d-a6b0-9b7b663aa49d/content

NL Times. (2025, 15 augustus). Homeless shelters for families bursting at the seams. *NL Times.* https://nltimes.nl/2025/08/15/homeless-shelters-families-bursting-seams

Oldebijvank, S. (2025, March 16). Organisatiestructuren Mintzberg | House of Control. *House of Control.* https://www.house-of-control.nl/organisatiestructuren-mintzberg-configuratie-coordinatiemechansimen-organisatietypen/

Pauluskerk Rotterdam. (z.d.). *De Pauluskerk.* https://www.pauluskerkrotterdam.nl/

Planije, M., Muusse, C., De Lange, A., Kroon, H., & Ministerie van Volksgezondheid, Welzijn en Sport. (2018). *Praktijktest landelijke toegankelijkheid maatschappelijke opvang.* https://www.trimbos.nl/wp-content/uploads/sites/31/2021/09/af1658-praktijktest-landelijke-toegankelijkheid-maatschappelijke-opvang-2018.pdf

Popper, K. (1959). *The Logic of Scientific Discovery.* Hutchinson.

VRIJWILLIGERS | Pauluskerk Rotterdam. (n.d.). https://www.pauluskerkrotterdam.nl/vrijwilligers/

Rasch, M. (2020). *Frictie: Ethiek in tijden van dataïsme.* De Bezige Bij.

Rijnmond. (2025, March 1). Dit is het profiel van daklozen in Rotterdam, maar een grote groep blijft buiten beeld. *Rijnmond.* https://www.rijnmond.nl/nieuws/1974507/dit-is-het-profiel-van-daklozen-in-rotterdam-maar-een-grote-groep-blijft-bu

Rotterdam Rekenkamer. (2023). *Opvolgingsonderzoek doorwerken aan daklozenopvang.* https://rekenkamer.rotterdam.nl/wp-content/uploads/2023/10/Doorwerken-aan-Daklozenopvang.pdf

STICHTING DIACONAAL CENTRUM PAULUSKERK ROTTERDAM. (2021). *JAARVERSLAG 2021 | PAULUSKERK ROTTERDAM.* https://netwerkdak.nl/wp-content/uploads/2022/12/DCPK_Jaarverslag2021.pdf

Trimbos-instituut. (2024b, October 7). *Mensen met een lichte verstandelijke beperking.* https://www.trimbos.nl/mensen-met-een-lichte-verstandelijke-beperking/

Wittgenstein, L. (1953). *Philosophical Investigations* (G. E. M. Anscombe, Vert.). Blackwell

Zien. (n.d.). *THDV - Wie Zie Jij?* https://www.thdv.nl/zien/dakloosheid/5/dakloosheid-in-nl-groeiend-probleem

Stichting Lezen en Schrijven. (2016, 1 mei). *Over de relatie tussen laaggeletterdheid en armoede.* https://www.lezenenschrijven.nl/wat-doen-wij/oplossing-voor-je-vraagstuk/over-de-relatie-tussen-laaggeletterdheid-en-armoede

Qwen Team. (2025). *Qwen3 technical report.* ArXiv. https://arxiv.org/abs/2505.09388
