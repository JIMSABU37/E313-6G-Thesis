import pandas as pd
from sklearn.ensemble import RandomForestRegressor

print("--- 6G Network Feature Importance Analysis ---")
print("Loading the full E313 Dataset (This might take a minute)...")
df = pd.read_csv("decisions-snapshots_pivot-filtered_20260122-130352.csv")

# 1. Target (What we want to predict)
target_col = 'latency_10'

# 2. Features (Take ALL columns except the target and the timestamp ID)
features = [col for col in df.columns if col not in ['decision_id', target_col]]

X = df[features]
y = df[target_col]

# FIX: Force X to only keep numbers, dropping the text-based timestamp!
X = X.select_dtypes(include=['number', 'float64', 'int64'])

# Update the features list to match the cleaned X
features = X.columns.tolist()

print(f"Analyzing {len(features)} different numeric network metrics simultaneously...")

# 3. Train the model to evaluate feature weight
model = RandomForestRegressor(n_estimators=50, max_depth=10, random_state=42)
model.fit(X, y)

# 4. Extract and Rank the Importance
importances = model.feature_importances_
feature_rank = pd.DataFrame({'Feature': features, 'Importance': importances})
feature_rank = feature_rank.sort_values('Importance', ascending=False).reset_index(drop=True)

print("\n--- TOP 10 MOST CRITICAL NETWORK METRICS ---")
print(feature_rank.head(10))

# 5. Save this to a CSV for your thesis report
feature_rank.to_csv("feature_importance_results.csv", index=False)
print("\nResults saved to 'feature_importance_results.csv'")