import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import joblib

# 1. Load data
df = pd.read_csv("decisions-snapshots_pivot-filtered_20260122-130352.csv")
data = df[['cpu_10', 'power_10', 'latency_10']].values

# 2. Normalize data (LSTMs are sensitive to scale)
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(data)

# 3. Create Sequences (Looking back at 10 time-steps to predict the next)
def create_sequences(data, seq_length):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i+seq_length, 0:2]) # Features: CPU, Power
        y.append(data[i+seq_length, 2])    # Target: Latency
    return np.array(X), np.array(y)

seq_length = 10 
X, y = create_sequences(scaled_data, seq_length)

# Split into train/test
train_size = int(len(X) * 0.8)
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# 4. Build the LSTM Architecture
model = Sequential([
    LSTM(50, activation='relu', input_shape=(seq_length, 2), return_sequences=True),
    Dropout(0.2),
    LSTM(20, activation='relu'),
    Dense(1)
])

model.compile(optimizer='adam', loss='mse')

# 5. Train the Model
print("Starting LSTM Training (Deep Learning Phase)...")
model.fit(X_train, y_train, epochs=5, batch_size=32, validation_split=0.1)

# 6. Save the LSTM Model and the Scaler
model.save("lstm_latency_model.keras")
joblib.dump(scaler, "data_scaler.pkl")
print("\nLSTM Model saved as 'lstm_latency_model.keras'")