import numpy as np
import pandas as pd
import psutil
import time
import socket
import joblib
import tensorflow as tf

# --- Configuration ---
INTERFACE = "WiFi"       # Your calibrated laptop interface name
SEQ_LENGTH = 10          # The history window your LSTM expects
UDP_IP = "127.0.0.1"     # Send to local receiver (or change to Pi's IP)
UDP_PORT = 5005
LATENCY_THRESHOLD = 0.0030  # Scaled danger threshold for the AI prediction

print("--- Experiment 3: Deploying AI Edge Controller ---")
print("Loading Deep Learning Brain and Scaler...")

# 1. Load the trained AI model and the data scaler
model = tf.keras.models.load_model("lstm_latency_model.keras")
scaler = joblib.load("data_scaler.pkl")

# 2. Set up the URLLC UDP Emergency Socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 3. Initialize the Sliding Window Buffer (10 steps of [CPU, Power])
# We will seed it with zeros to start
history_buffer = []

print(f"AI Edge Controller Live. Monitoring interface: {INTERFACE}...")

try:
    while True:
        # A. SENSE: Gather live hardware metrics
        net_io_1 = psutil.net_io_counters(pernic=True)
        cpu_usage = psutil.cpu_percent()
        
        # We simulate the power usage pattern found in your dataset analysis
        # When CPU load climbs, power increases proportionally
        simulated_power = 61.07 + (cpu_usage * 0.1) 
        
        # Add the current snapshot to our history buffer
        history_buffer.append([cpu_usage, simulated_power])
        
        # Keep the buffer fixed at exactly the last 10 seconds
        if len(history_buffer) > SEQ_LENGTH:
            history_buffer.pop(0)
            
        # B. THINK: Once the buffer is full, let the AI analyze the sequence
        if len(history_buffer) == SEQ_LENGTH:
            # Prepare data format for the LSTM
            input_data = np.array(history_buffer)
            
            # Use the scaler dummy to format features properly for the network
            # (LSTM expects scaled data between 0 and 1)
            dummy_matrix = np.zeros((SEQ_LENGTH, 3))
            dummy_matrix[:, 0:2] = input_data
            scaled_matrix = scaler.transform(dummy_matrix)
            
            # Reshape for TensorFlow input: [Batch_Size, Time_Steps, Features]
            lstm_input = np.expand_dims(scaled_matrix[:, 0:2], axis=0)
            
            # C. PREDICT: Run inference
            predicted_latency_scaled = model.predict(lstm_input, verbose=0)[0][0]
            
            print(f"[MONITOR] CPU: {cpu_usage:.1f}% | Sim_Power: {simulated_power:.2f} | Pred_Loss_Scale: {predicted_latency_scaled:.4f}")
            
            # D. ACT: Proactive Congestion Management
            if predicted_latency_scaled > LATENCY_THRESHOLD:
                msg = f"CRITICAL: AI predicted latency anomaly! Scaled Value: {predicted_latency_scaled:.4f}"
                sock.sendto(msg.encode('utf-8'), (UDP_IP, UDP_PORT))
                print(f"⚠️  [URLLC TRIGGER] Safety message dispatched to Edge Node!")
                
        time.sleep(1)

except KeyboardInterrupt:
    print("\nAI Edge Controller Terminated Cleanly.")