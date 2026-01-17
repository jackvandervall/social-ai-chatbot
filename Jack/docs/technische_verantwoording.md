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
| Synthetische SFT | Multi-turn conversaties | NL/EN/PL/AR | 10 |
| DPO Preference Pairs | Prompt + Chosen + Rejected | NL/EN/PL/AR | 20 |

### Teacher-Model voor Synthese
**DeepSeek V3.2** via OpenRouter API.

**Motivatie:**
- Kostenefficiënt (~$0.25-0.38/1M tokens) vergeleken met GPT-4o ($5-$15/1M)
- Uitstekende meertalige capaciteiten (Nederlands, Pools, Arabisch)
- Native JSON-output ondersteuning
- Open-weight model, transparant gedrag

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
| `load_in_4bit` | True | QLoRA voor 6GB GPU |

**Motivatie:**
- Slechts ~0.1% van parameters getraind
- Voorkomt catastrophic forgetting van basiskennis
- Mogelijk op consumer hardware (RTX 3060 6GB)

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

## 4. Modelkeuze

### Basismodel
**Qwen3-8B-Instruct** (4-bit quantized via Unsloth)

**Motivatie:**
| Criterium | Qwen3-8B | Llama 3-8B | Mistral 7B |
|-----------|----------|------------|------------|
| Meertalig (NL/PL/AR) | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ |
| Instructie-volgen | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| VRAM (4-bit) | 6GB | 6GB | 5GB |
| Unsloth support | ✅ | ✅ | ✅ |
| Licentie | Apache 2.0 | Llama 3 License | Apache 2.0 |

Qwen3 scoort het beste op **niet-Engelse talen**, specifiek relevant voor onze Pools- en Arabisch-sprekende doelgroep.

### Deployment Formaat
**GGUF Q4_K_M** voor lokale inference via LMStudio.

---

## 5. Samenvatting Technische Stack

```
┌─────────────────────────────────────────────────────────┐
│                    DATA GENERATIE                       │
│  DeepSeek V3 → OpenRouter API → JSONL (SFT + DPO)      │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                    FINE-TUNING                          │
│  Qwen3-8B + Unsloth + LoRA + TRL SFTTrainer            │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                    ALIGNMENT                            │
│  TRL DPOTrainer + Preference Data                       │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                    DEPLOYMENT                           │
│  GGUF Q4_K_M → LMStudio / Ollama                        │
└─────────────────────────────────────────────────────────┘
```

---

## Referenties

1. Hu, E. et al. (2021). *LoRA: Low-Rank Adaptation of Large Language Models*. arXiv:2106.09685
2. Rafailov, R. et al. (2023). *Direct Preference Optimization*. arXiv:2305.18290
3. Unsloth Documentation: https://docs.unsloth.ai/
4. Qwen3 Technical Report: https://qwenlm.github.io/blog/qwen3/
