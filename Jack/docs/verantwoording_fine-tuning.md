# Technische Verantwoording – RotterMaatje Fine-Tuning Pipeline

## Overzicht

Dit document beschrijft de technische keuzes voor het trainen van een domein-specifiek taalmodel voor RotterMaatje: een chatbot die daklozen in Rotterdam ondersteunt bij het vinden van opvang, voedsel en medische zorg.

De pipeline bestaat uit drie fasen:

```
┌────────────────┐    ┌────────────────┐    ┌────────────────┐
│  1. Data       │ -> │  2. Fine-Tune  │ -> │  3. RL/DPO     │
│  Generatie     │    │  (SFT)         │    │  Alignment     │
└────────────────┘    └────────────────┘    └────────────────┘
```

---

## 1. Data Generatie

### Aanpak
Combinatie van **echte FAQ-data** en **synthetische data** gegenereerd door een teacher-model.

| Databron | Formaat | Taal | Voorbeelden |
|----------|---------|------|-------------|
| `faq_structured.json` | Q&A paren | Nederlands | 24 |
| `apv_structured.json` | Q&A paren | Nederlands | 8 |
| Synthetische SFT | Multi-turn conversaties | NL/EN/PL/AR | 50 (rewritten) |
| DPO Preference Pairs | Prompt + Chosen + Rejected | NL/EN/PL/AR | 50 |

### Teacher-Model voor Synthese
**Deepseek V3.2** (via OpenRouter) of **Grok-4.1-fast**.

**Motivatie:**
- **Deepseek V3.2:** Gebruikt voor grootschalige data-generatie vanwege lage kosten en meertalige kracht.
- **Grok-4.1-fast:** Gebruikt in de testfase voor snelle validatie van prompts en agentic tool-calling gedrag.
- **Privacy Guardrail:** Synthetische data bevat GEEN echte persoonsgegevens van cliënten (GDPR/AVG compliant).

### DPO Negatieve Voorbeelden
De "rejected" antwoorden bevatten bewust fouten:
1. **Verkeerde adressen** (Pauluskerk ↔ NAS verwisseling)
2. **Verkeerde taal** (Nederlands antwoord op Poolse vraag)
3. **Onvriendelijke toon**
4. **Gehalluceerde informatie**

---

## 2. Supervised Fine-Tuning (SFT)

### Framework
**Unsloth** + **Hugging Face TRL (SFTTrainer)**

**Motivatie voor Unsloth:**
- 2x snellere training dan standaard Hugging Face
- 70% minder VRAM-gebruik door kernel-optimalisaties
- Native ondersteuning voor 4-bit quantisatie (QLoRA)
- Directe GGUF export voor LMStudio/Ollama deployment

### Parameter-Efficient Fine-Tuning (PEFT)
**LoRA (Low-Rank Adaptation)** in plaats van volledige fine-tuning.

| Parameter | Waarde | Toelichting |
|-----------|--------|-------------|
| `r` (rank) | 16 | Balans tussen capaciteit en VRAM |
| `lora_alpha` | 16 | Scaling factor |
| `target_modules` | q/k/v/o_proj, gate/up/down_proj | Alle attention + MLP lagen |
| `load_in_4bit` | True | QLoRA voor 4GB GPU (RTX 3050) |

**Motivatie:**
- Slechts ~0.1% van parameters getraind
- Voorkomt catastrophic forgetting van basiskennis
- Cruciaal voor hardware met **4GB VRAM** (RTX 3050)

### Trainingsparameters

| Parameter | Waarde |
|-----------|--------|
| Batch size | 1 |
| Gradient accumulation | 8 |
| Learning rate | 2e-4 |
| Max steps | 60 |
| Optimizer | AdamW 8-bit |

---

## 3. Reinforcement Learning – Direct Preference Optimization (DPO)

### Framework
**TRL DPOTrainer** met Unsloth integratie.

### Waarom DPO in plaats van RLHF?
| Aspect | RLHF | DPO |
|--------|------|-----|
| Complexiteit | Hoog (reward model + PPO) | Laag (directe preference loss) |
| Stabiliteit | Instabiel, hyperparameter-gevoelig | Stabiel, minder tuning nodig |
| Kosten | 2x meer GPU-tijd | Vergelijkbaar met SFT |
| Data | Vereist reward scores | Alleen preference pairs |

**DPO Loss Functie:**
```
L_DPO = -log σ(β · (log π(y_w|x) - log π(y_l|x)))
```
Waarbij `y_w` = chosen, `y_l` = rejected, `β` = 0.1 (KL-penalty)

### Trainingsparameters

| Parameter | Waarde |
|-----------|--------|
| β (beta) | 0.1 |
| Learning rate | 5e-6 |
| Max prompt length | 512 |
| Max total length | 1024 |

---

## 4. Modelkeuze & Architectuur

### Lokale Fine-Tune: qwen3-4b-2507 (GGUF)
Gekozen voor de **4B variant** in plaats van 8B vanwege de hardware restrictie (**RTX 3050 4GB VRAM**).

| Criterium | Qwen3-4B | Llama 3.2-3B | Gemma 3-4B |
|-----------|----------|--------------|------------|
| VRAM Vulling | ⭐⭐⭐ (Volledig in VRAM) | ⭐⭐⭐ | ⭐⭐ (Krap) |
| Meertalig | ⭐⭐⭐ | ⭐ | ⭐⭐ |
| Redeneren | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ |

### Productie Gatekeeper: Safeguard-20b
Voor de **triage-fase** wordt een groter, extern model gebruikt: **gpt-oss-safeguard-20b**.
- **Doel:** Filteren van onveilige input, detectie van crisis/spoedgevallen.
- **Transparantie:** Volledige *chain-of-thought* voor auditbaarheid.

### Productie Agent: Grok-4.1-fast
Voor de **interactie met tools** (VectorDB, agenda, services) wordt **Grok-4.1-fast** gebruikt.
- **Reden:** Extreem lage latency en superieure tool-calling prestaties voor complexe agentic workflows.

### Deployment Formaat
**GGUF Q4_K_M** voor de lokale 4B-component via LMStudio/Ollama.

---

## 5. Samenvatting Technische Stack

```
┌─────────────────────────────────────────────────────────┐
│                    DATA GENERATIE                       │
│  Deepseek V3.2.2 → JSONL (50 SFT + 50 DPO)                  │
│  *Softened persona via core/prompts.py*                 │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                    FINE-TUNING (LOCAL)                  │
│  Qwen3-4B + Unsloth + LoRA (RTX 3050 Optimized)         │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                    HYBRIDE ARCHITECTUUR                 │
│ 1. Safeguard-20b (Triage)                               │
│ 2. Grok-4.1-fast (Tool Orchestrator)                    │
│ 3. Qwen3-4B (Local Persona & Logic)                     │
└─────────────────────────────────────────────────────────┘
```

---

## Referenties

1. Hu, E. et al. (2021). *LoRA: Low-Rank Adaptation of Large Language Models*. arXiv:2106.09685
2. Rafailov, R. et al. (2023). *Direct Preference Optimization*. arXiv:2305.18290
3. Unsloth Documentation: https://docs.unsloth.ai/
4. Qwen3 Technical Report: https://qwenlm.github.io/blog/qwen3/
