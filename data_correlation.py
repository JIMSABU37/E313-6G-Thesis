import pandas as pd

df = pd.read_csv("decisions-snapshots_pivot-filtered_20260122-130352.csv")

# We want to see how Power and CPU impact Latency
# Let's check Node 10 specifically as it has high latency
correlation_matrix = df[['cpu_10', 'power_10', 'latency_10']].corr()

print("--- Correlation Analysis (Scientific Basis) ---")
print("How much do these factors impact Latency? (1.0 is a perfect match)")
print(correlation_matrix['latency_10'])

# Let's find the "Danger Zone"
danger_zone = df[df['latency_10'] > 500] # Latency over 500ms
print(f"\nNumber of 'Danger Zone' events: {len(danger_zone)}")
print(f"Average Power during Danger: {danger_zone['power_10'].mean():.2f}")
print(f"Average Power during Normal: {df[df['latency_10'] <= 500]['power_10'].mean():.2f}")