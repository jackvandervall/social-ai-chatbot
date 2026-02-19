# RotterMaatje fine-tuning experiment: exp001_baseline_rottermaatj

## Technisch overzicht
1. Datavolume & Structuur
SFT (Supervised Fine-Tuning): 49 voorbeelden in .jsonl formaat.
Structuur: Gesprekken met meerdere beurten (User/Assistant).
DPO (Direct Preference Optimization): 50 voorbeelden in .jsonl formaat.
Structuur: Prompt-Chosen-Rejected triplets voor reinforcement learning.

2. Bron & Generatie
Kennisbron: Gebaseerd op faq_structured.json en apv_structured.json (lokale Rotterdamse regelgeving en hulpdiensten).
Engine: Synthetische generatie via DeepSeek V3.2 (OpenRouter).
Techniek: LLM-herschrijving van ruwe juridische/FAQ-tekst naar een empathische persona op "B1-niveau".

3. Meertaligheid
Taalverdeling: Verdeeld over Nederlands (nl), Engels (en), Pools (pl) en Arabisch (ar).
Doel: Toegankelijkheid waarborgen voor anderstalige daklozen en vrijwilligers.

4. Onderwerpen
Nachtopvang en Winteropvang (NAS, Zestienhoven).
Basisvoorzieningen (eten bij Pauluskerk, douches, kleding).
Juridische zaken (BSN aanvraag, RNI-loket, briefadres).
APV-regels (alcoholgebruik op straat, hinderlijk ophouden).

## Synthetic data generation
Vandaag heb ik data gegenereerd om het qwen3-4b-instruct model te fine-tunen. Om de data te generenen heb ik Deepseek V3.2 gebruikt voor data-generatie vanwege lage kosten en meertalige kracht. De data is gegenereerd op basis van reële interacties en topics vanuit de data in de interne kennisbank. Daarnaast is ook DPO reinforcement learning toegepast, waardoor de LLM ook leert om een foutieve toon en incorrecte data te vermijden. 

## Technische restricties
Helaas kon ik het model niet lokaal trainen, zelfs niet met quantization, vanwege deze error:

>"ValueError: Some modules are dispatched on the CPU or the disk. Make sure you have enough GPU RAM to fit the quantized model."

Vandaar dat ik het fine-tunen en de reinforcement learning via Google Colab heb gedaan. 


## Resultaten

🧪 Testing fine-tuned model:
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

## Bevindingen
Zoals te zien is uit de test output, geeft het model op empathische manier antwoord (bijv. "Ik begrijp dat het moeilijk is"), en kan het ook in verschillende talen antwoorden (bijv. Arabisch:"مرحبًا! نعم، يمكنني مساعدتك."). De data die is gebruikt voor het fine-tunen, afkomstig uit de interne kennisbank, kwam ook terug in de test output.

## Hallucinaties
Er is alleen een merkwaardig antwoord gegenereerd, waarin de LLM ervan uit lijkt te gaan dat de user uit de gevangenis komt, in tegenstelling tot de initiële prompt, waarbij de user dakloos is en honger heeft. Dit kan komen door de data die is gebruikt voor het fine-tunen, waarbij een klein deel van de trainingsdata specifiek over "ex-gedetineerden" ging, waardoor mogelijk een overfit voor deze hallucinatie heeft gezorgt.  

Voorbeeld van de data die is gebruikt:

> "{"messages": [{"role": "user", "content": "Hoi, ik ben een vrijwilliger bij de Pauluskerk. Er is net iemand binnen gekomen die uit de gevangenis komt en vraagt waar hij kan slapen. Kun je helpen?"}, {"role": "assistant", "content": "Hallo, bedankt voor je vraag. Ik wil graag helpen. Is deze persoon ingeschreven in de gemeente Rotterdam? Dit is belangrijk om te weten voor de juiste opvang."}, {"role": "user", "content": "Ja, hij is ingeschreven in Rotterdam."}, {"role": "assistant", "content": "Dat is goed om te weten. Hij kan zich melden bij de Reclassering en de gemeente Rotterdam. Het adres is Delftseplein 29. Daar kunnen ze hem verder helpen met een plek om te slapen en andere ondersteuning. Zijn er nog andere dingen waar hij hulp bij nodig heeft, zoals medische zorg of hulp bij verslaving?"}]}"

Om dit te voorkomen is het belangrijk om diverse data te hebben voor het fine-tunen om deze bias te voorkomen. In de volgende experimenten zal ik hier rekening mee houden en een grotere hoeveelheid data genereren in verschillende scenario's om de betrouwbaarheid van het model te vergroten.