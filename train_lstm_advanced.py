import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import pickle

print("--- 6G PROACTIVE AI: ADVANCED CROSS-NODE BRAIN ---")
print("Loading the full E313 Dataset...")

df = pd.read_csv("decisions-snapshots_pivot-filtered_20260122-130352.csv")

# The Top 6 Features
features = ['power_10', 'cpu_10', 'cpu_8', 'latency_8', 'latency_6', 'selected node']
target = 'latency_10'

data_X = df[features].values
data_y = df[target].values

print(f"Training on the Top {len(features)} Features...")

scaler_X = MinMaxScaler()
scaler_y = MinMaxScaler()

data_X_scaled = scaler_X.fit_transform(data_X)
data_y_scaled = scaler_y.fit_transform(data_y.reshape(-1, 1))

def create_sequences(X, y, time_steps=10):
    Xs, ys = [], []
    for i in range(len(X) - time_steps):
        Xs.append(X[i:(i + time_steps)])
        ys.append(y[i + time_steps])
    return np.array(Xs), np.array(ys)

time_steps = 10
X_seq, y_seq = create_sequences(data_X_scaled, data_y_scaled, time_steps)

model = Sequential([
    LSTM(32, activation='relu', input_shape=(X_seq.shape[1], X_seq.shape[2])),
    Dropout(0.2),
    Dense(16, activation='relu'),
    Dense(1, activation='linear')
])

model.compile(optimizer='adam', loss='mse')

print("Training Advanced Model...")
history = model.fit(X_seq, y_seq, epochs=3, batch_size=64, validation_split=0.2)

# ISOLATING THE FILES: Saving with new names!
model.save("lstm_advanced.keras")
with open("scaler_advanced.pkl", "wb") as f:
    pickle.dump(scaler_X, f)

print("\n✅ UPGRADE COMPLETE: Saved as 'lstm_advanced.keras'!")
import matplotlib.pyplot as plt
import seaborn as sns

print("Generating Training Curve Graph...")

# Set up the visual style
sns.set_theme(style="whitegrid")
plt.figure(figsize=(8, 6))

# Plot the training and validation loss from the 'history' object
# (Make sure your model.fit() was saved to a variable called 'history')
plt.plot(history.history['loss'], label='Training Loss', color='blue', linewidth=2)
plt.plot(history.history['val_loss'], label='Validation Loss', color='orange', linewidth=2)

plt.title("LSTM Model Learning Curve: Training vs. Validation Loss", fontsize=14, fontweight='bold')
plt.xlabel("Epochs", fontsize=12, fontweight='bold')
plt.ylabel("Loss (Mean Squared Error)", fontsize=12, fontweight='bold')
plt.legend(loc="upper right")

# Save the graph
plt.tight_layout()
plt.savefig("thesis_graph_training_curve.png", dpi=300)
print("✅ SUCCESS: Graph saved as 'thesis_graph_training_curve.png'!")
