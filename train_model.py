import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib

# 1. Load the data
print("Loading E313 Dataset...")
df = pd.read_csv("decisions-snapshots_pivot-filtered_20260122-130352.csv")

# 2. Feature Selection (The 'Scientific Basis')
# We use CPU and Power to predict Latency
features = ['cpu_10', 'power_10']
target = 'latency_10'

X = df[features]
y = df[target]

# 3. Split data (80% for training, 20% for testing the AI's accuracy)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Initialize and Train the TinyML Model
print("Training the Predictive Model (Random Forest)...")
model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
model.fit(X_train, y_train)

# 5. Validate the Model
predictions = model.predict(X_test)
error = mean_absolute_error(y_test, predictions)

print(f"\n--- Model Training Complete ---")
print(f"Mean Absolute Error: {error:.2f} ms")
print(f"The model can predict latency within +/- {error:.2f} milliseconds.")

# 6. Save the model to a file (The 'Brain' file)
joblib.dump(model, "latency_predictor_model.pkl")
print("\nModel saved as 'latency_predictor_model.pkl'")