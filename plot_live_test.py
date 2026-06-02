import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("--- Generating Live Physical Test Graph ---")

# 1. Load the recorded data
df = pd.read_csv("live_physical_test_results.csv")

# 2. Set up the visual style for an academic paper
sns.set_theme(style="whitegrid")
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# 3. Top Graph: Hardware Telemetry (CPU)
ax1.plot(df['Time_Seconds'], df['Node10_CPU'], color='blue', linewidth=2, label='Node10 CPU (%)')
ax1.axhline(50.0, color='orange', linestyle='--', label='Simulated Fault Threshold (50%)')
ax1.set_ylabel("CPU Usage (%)", fontsize=12, fontweight='bold')
ax1.set_title("6G Edge AI Testbed: Telemetry & Proactive Trigger Response", fontsize=14, fontweight='bold')

# MOVED SLIGHTLY LEFT INTO THE PERFECT DEAD SPACE
ax1.legend(loc="upper center", bbox_to_anchor=(0.4, 1.0))

# 4. Bottom Graph: AI Prediction & UDP Triggers
ax2.plot(df['Time_Seconds'], df['Pred_Risk'], color='red', linewidth=2, label='AI Predicted Risk (Latency)')
ax2.axhline(0.0042, color='darkred', linestyle='--', label='URLLC Safety Threshold (0.0042)')

# Highlight the exact moments the UDP trigger fired
triggers = df[df['Trigger_Fired'] == 1]
ax2.scatter(triggers['Time_Seconds'], triggers['Pred_Risk'], color='black', marker='X', s=100, label='UDP Trigger Dispatched')

ax2.set_xlabel("Time (Seconds)", fontsize=12, fontweight='bold')
ax2.set_ylabel("Predicted Latency Risk", fontsize=12, fontweight='bold')

# MOVED SLIGHTLY LEFT INTO THE PERFECT DEAD SPACE
ax2.legend(loc="upper center", bbox_to_anchor=(0.4, 1.0))

# 5. Save the graph as a high-resolution image
plt.tight_layout()
plt.savefig("thesis_graph_live_test.png", dpi=300)

print("✅ SUCCESS: Graph saved as 'thesis_graph_live_test.png'!")