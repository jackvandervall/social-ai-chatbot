## Daily Logs
---
27-11-2025
Initiële setup met gebruikerspecifieke en gezamenlijke folderstructuur en uv packet manager initialisatie voor efficiënt beheer van libraries.

01-12-2025
example_evaluating_llm.ipynb en environment variabelen aangepast zodat ik CUDA kon gebruiken om llm's op mijn gpu te kunnen runnen. Verder nog verschillende prompts getest op de 3 llm's in de example Python file: QWEN3: 0.6, 0.6-base en 4B. Daarnaast een proof-of-concept agent met basic system prompt en mock database aangemaakt.

02-12-2025
Proof-of-concept agent.py aangepast om deepseek/deepseek-v3.2 te gebruiken, getest op verschillende talen als Engels, Nederlands, Arabisch en Pools waaruit blijkt dat dit model een goed begrip heeft van diverse talen. Dit model heeft ook een ruime context window van 163K, helaas is het niet mogelijk om dit te fine-tunen vanwege de grootte van het model, maar we zouden het kunnen gebruiken als testmodel om later een gedistilleerd deepseek model te fine-tunen zoals deepseek-r1-distill-llama-8b of deepseek-r1-distill-qwen-32b.

Om de agent te voorzien van een robuuste system prompt, guardrails en veiligheidsdisclaimers is de prompts.py file aangemaakt. De prompts.py file heeft de volgende voordelen:

- Versiebeheer: Track prompt aanpassingen los van de agent architecture
- A/B Testing: Gemakkelijk prompt configuraties testen en vergelijken
- Snelle iteratie: Update prompts zonder de code te hoeven aanpassen