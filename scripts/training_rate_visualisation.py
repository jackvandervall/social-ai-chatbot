import matplotlib.pyplot as plt
import numpy as np

# --- DATA FROM YOUR LOGS ---
# SFT Data
sft_steps = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
sft_loss = [2.7044, 1.8855, 1.5796, 1.4338, 1.3517, 1.2801, 1.2153, 1.1499, 1.0497, 1.0317, 
            1.0302, 0.9879, 0.9971, 0.9302, 0.9015, 0.8491, 0.8779, 0.8223, 0.8356, 0.7947]

# DPO Data
dpo_steps = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]
dpo_loss = [0.0775, 0.0973, 0.0684, 0.1116, 0.1533, 0.0281, 0.0632, 0.0848, 0.1109, 0.0449, 0.0379, 0.0708]
# Margins = Chosen Reward - Rejected Reward (The most important metric in DPO)
dpo_margins = [5.08, 5.47, 5.49, 4.50, 4.29, 6.20, 5.98, 5.04, 5.79, 5.06, 6.07, 4.90]
dpo_accuracy = [1.0, 0.95, 0.975, 0.975, 0.975, 1.0, 1.0, 1.0, 0.975, 1.0, 1.0, 0.975]

# --- PLOTTING SETUP ---
plt.style.use('dark_background') # Matches HF Dark Mode
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5))

# Plot 1: SFT Convergence
ax1.plot(sft_steps, sft_loss, color='#FF9D00', linewidth=2.5, marker='o', markersize=4)
ax1.set_title('Stage 1: SFT Loss Convergence', fontsize=12, fontweight='bold')
ax1.set_xlabel('Steps')
ax1.set_ylabel('Loss')
ax1.grid(color='#333333', linestyle='--')

# Plot 2: DPO Margins (The "Proof it Works" Graph)
ax2.plot(dpo_steps, dpo_margins, color='#00FF00', linewidth=2.5, marker='s', markersize=4)
ax2.set_title('Stage 2: DPO Margin (Chosen - Rejected)', fontsize=12, fontweight='bold')
ax2.set_xlabel('Steps')
ax2.set_ylabel('Margin Score')
ax2.grid(color='#333333', linestyle='--')

# Plot 3: DPO Accuracy
ax3.plot(dpo_steps, dpo_accuracy, color='#00CCFF', linewidth=2.5)
ax3.set_title('Stage 2: DPO Accuracy', fontsize=12, fontweight='bold')
ax3.set_xlabel('Steps')
ax3.set_ylabel('Accuracy (0-1)')
ax3.set_ylim(0.9, 1.02)
ax3.grid(color='#333333', linestyle='--')

plt.tight_layout()
plt.savefig('training_metrics.png', dpi=300, bbox_inches='tight')
print("Graph saved as training_metrics.png")