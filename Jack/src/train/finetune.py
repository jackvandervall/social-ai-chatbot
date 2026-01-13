"""
Supervised Fine-Tuning (SFT) script for the RotterMaatje chatbot.

This script uses the Unsloth framework to fine-tune a Qwen3-8B model 
on conversational data using LoRA (Low-Rank Adaptation).
"""

from unsloth import FastLanguageModel
import torch
from trl import SFTTrainer
from transformers import TrainingArguments
from datasets import load_dataset
from unsloth.chat_templates import get_chat_template
import os

# 1. Load Model & Tokenizer
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "unsloth/Qwen3-8B-bnb-4bit",
    max_seq_length = 1024, # Reduced from 2048 for 6GB VRAM
    load_in_4bit = True,
)

# Setup Chat Template
tokenizer = get_chat_template(
    tokenizer,
    chat_template = "qwen-2.5", # Mapping Qwen3 to Qwen2.5/ChatML format
)

# 2. Add PEFT (LoRA) adapters
model = FastLanguageModel.get_peft_model(
    model,
    r = 16, # Higher r = more "memory" of new data, but more VRAM
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
                      "gate_proj", "up_proj", "down_proj",],
    lora_alpha = 16,
    lora_dropout = 0, # Optimized for 0 by Unsloth
    bias = "none",    
    use_gradient_checkpointing = "unsloth", 
)

# Load Dataset
if os.path.exists("Jack/data/synthetic_train.jsonl"):
    data_path = "Jack/data/synthetic_train.jsonl"
else:
    data_path = "Jack/data/dummy_data.jsonl"
dataset = load_dataset("json", data_files=data_path, split="train")

def formatting_prompts_func(examples):
    """
    Formats conversational sequences into a chat-template compatible string.

    Args:
        examples (dict): A batch of examples containing 'messages'.

    Returns:
        dict: A dictionary with the formatted 'text' field.
    """
    convos = examples["messages"]
    texts = [tokenizer.apply_chat_template(convo, tokenize=False, add_generation_prompt=False) for convo in convos]
    return { "text" : texts, }

dataset = dataset.map(formatting_prompts_func, batched = True,)

# 3. Training Config (SFT)
trainer = SFTTrainer(
    model = model,
    tokenizer = tokenizer,
    train_dataset = dataset,
    dataset_text_field = "text",
    max_seq_length = 1024,
    dataset_num_proc = 2,
    packing = False, # Can make training 5x faster for short sequences.
    args = TrainingArguments(
        per_device_train_batch_size = 1, # Reduced from 2 for 6GB VRAM
        gradient_accumulation_steps = 8, # Increased to maintain effective batch size
        warmup_steps = 5,
        max_steps = 60, # For testing; increase for production
        learning_rate = 2e-4,
        fp16 = not torch.cuda.is_bf16_supported(),
        bf16 = torch.cuda.is_bf16_supported(),
        logging_steps = 1,
        weight_decay = 0.01,
        output_dir = "outputs",
        optim = "adamw_8bit",
        seed = 3407,
    ),
)

# 4. Train
trainer_stats = trainer.train()

# 5. Save for RotterMaatje UI
model.save_pretrained_gguf("model_q4_k_m", tokenizer, quantization_method = "q4_k_m")
