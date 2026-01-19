"""
Reinforcement Learning via Direct Preference Optimization (DPO) for RotterMaatje.

This script aligns the fine-tuned model with specific safety and accuracy 
preferences using preference pairs (chosen vs. rejected responses).
"""

from unsloth import FastLanguageModel, PatchDPOTrainer
from transformers import TrainingArguments
from trl import DPOTrainer
from datasets import load_dataset
import torch
import os

# Patch DPO for Unsloth speedups
PatchDPOTrainer()

# 1. Load Model & Tokenizer
# Typically we would load the LoRA weights from the SFT stage first,
# but for this script we show how to do DPO on a base or SFT-aligned model.
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "Qwen/Qwen3-4B-Instruct-2507", # Or your SFT checkpoint "outputs/checkpoint-X"
    max_seq_length = 2048,
    load_in_4bit = True,
)

# 2. Add PEFT (LoRA) adapters
model = FastLanguageModel.get_peft_model(
    model,
    r = 16,
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
                      "gate_proj", "up_proj", "down_proj",],
    lora_alpha = 16,
    lora_dropout = 0,
    bias = "none",    
    use_gradient_checkpointing = "unsloth",
)

# 3. Load DPO Dataset
dataset = load_dataset("json", data_files="Jack/data/synthetic_dpo.jsonl", split="train")

# 4. Training Config (DPO)
dpo_trainer = DPOTrainer(
    model = model,
    ref_model = None, # Unsloth handles this automatically for PEFT
    args = TrainingArguments(
        per_device_train_batch_size = 1,
        gradient_accumulation_steps = 8,
        warmup_steps = 5,
        max_steps = 40, # Short run for demonstration
        learning_rate = 5e-6, # DPO learning rate is usually lower than SFT
        fp16 = not torch.cuda.is_bf16_supported(),
        bf16 = torch.cuda.is_bf16_supported(),
        logging_steps = 1,
        optim = "adamw_8bit",
        weight_decay = 0.05,
        output_dir = "outputs_dpo",
        seed = 3407,
    ),
    beta = 0.1, # The 'beta' parameter for DPO (KL penalty)
    train_dataset = dataset,
    tokenizer = tokenizer,
    max_length = 1024,
    max_prompt_length = 512,
)

# 5. Train
dpo_trainer.train()

# 6. Save
model.save_pretrained_gguf("model_final_dpo", tokenizer, quantization_method = "q4_k_m")
print("DPO Training complete and model saved as GGUF.")
