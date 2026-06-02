import time
import socket
import psutil
import numpy as np
import pickle
import warnings
import os
import csv
from tensorflow.keras.models import load_model

warnings.filterwarnings('ignore')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

print("--- 6G Smart Highway: ADVANCED Cross-Node Controller ---")

model = load_model("lstm_advanced.keras")
with open("scaler_advanced.pkl", "rb") as f:
    scaler = pickle.load(f)

# TARGET IP: Change this to your Raspberry Pi's IP!
UDP_IP = "192.168.1.83" 
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

history_window = []
TIME_STEPS = 10
LATENCY_THRESHOLD = 0.0050  

# Create the CSV file to log data for your thesis graphs
csv_filename = "live_physical_test_results.csv"
with open(csv_filename, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Time_Seconds", "Node10_CPU", "Pred_Risk", "Trigger_Fired"])

print(f"Monitoring 6-Feature Cross-Node Telemetry. Logging to {csv_filename}...")
start_time = time.time()

try:
    while True:
        # 1. Real Local Hardware Metrics
        cpu_10 = psutil.cpu_percent()
        power_10 = 60.0 + (cpu_10 * 0.1) 
        
        # 2. Dynamic Simulated Cross-Node Domino Effect (Fault Injection)
        if cpu_10 > 50.0:
            # When your laptop chokes, simulate the neighboring nodes crashing!
            cpu_8, latency_8, latency_6, selected_node = 85.0, 45.0, 30.0, 8.0
        else:
            # Normal, calm network traffic
            cpu_8, latency_8, latency_6, selected_node = 25.0, 5.0, 4.0, 10.0
            
        current_metrics = [power_10, cpu_10, cpu_8, latency_8, latency_6, selected_node]
        history_window.append(current_metrics)
        
        if len(history_window) > TIME_STEPS:
            history_window.pop(0)
            
            input_data = np.array(history_window)
            input_scaled = scaler.transform(input_data)
            input_reshaped = input_scaled.reshape(1, TIME_STEPS, 6) 
            
            pred_latency = model.predict(input_reshaped, verbose=0)[0][0]
            
            trigger_status = 0
            if pred_latency > LATENCY_THRESHOLD:
                print("⚠️  [URLLC TRIGGER] Firing UDP over Air Interface to Pi!")
                sock.sendto(b"URLLC_EMERGENCY_REROUTE", (UDP_IP, UDP_PORT))
                trigger_status = 1
            else:
                print(f"[MONITOR] Local CPU: {cpu_10}% | Pred_Risk: {pred_latency:.4f}")
            
            # Log the data for the graph
            elapsed_time = round(time.time() - start_time, 2)
            with open(csv_filename, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([elapsed_time, cpu_10, pred_latency, trigger_status])
                
        time.sleep(1)

except KeyboardInterrupt:
    print(f"\nTest complete. Data saved to {csv_filename} for graphing.")