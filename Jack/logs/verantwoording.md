### Hardware Snapshot
* **Laptop:** ASUS TUF Gaming A15 (Model FA506ICB)
* **GPU:** **NVIDIA GeForce RTX 3050** (4 GB VRAM)
    * *Note:* This specific ASUS model uses the newer **RTX** 3050. This is better; it supports DLSS and Tensor cores, though the 4 GB VRAM remains the strict limit.
* **Bottleneck:** **4 GB VRAM.**
    * Models under 4 GB run instantly (GPU only).
    * Models over 4 GB (like 7B/8B) spill into system RAM, causing significant slowdowns.

### Recommended Models (Ranked for 4 GB VRAM)
* **Best Overall (Balance):** **Gemma 3 4B Instruct** (Q4 Quantization)
    * Fits fully in VRAM (~3.0 GB).
    * Best mix of speed and smarts for this specific laptop.
* **Best for Speed:** **Llama 3.2 3B Instruct** (Q6 or Q8 Quantization)
    * Uses less VRAM (~2.5 GB).
    * Extremely snappy; great for quick chats and roleplay.
* **Best for Coding/Logic:** **Qwen2.5-Coder 3B**
    * Punches above its weight for programming tasks while staying fast.
* **Best for Complex Reasoning (Slow):** **Phi-3.5 Mini** (3.8B) or **Qwen 2.5 7B**
    * Phi-3.5 is incredibly smart but pushes the 4 GB limit to the edge.
    * Qwen 7B will run slowly (via RAM offload) but is necessary for "deep thought" research.