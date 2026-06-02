import time
import socket
import psutil
import numpy as np
import pickle
import warnings
import os
from tensorflow.keras.models import load_model

warnings.filterwarnings('ignore')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

print("--- 6G Smart Highway: ADVANCED Cross-Node Controller ---")

# ISOLATED: Loading the new advanced files!
model = load_model("lstm_advanced.keras")
with open("scaler_advanced.pkl", "rb") as f:
    scaler = pickle.load(f)

UDP_IP = "127.0.0.1" 
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

history_window = []
TIME_STEPS = 10
LATENCY_THRESHOLD = 0.0030  

print("Monitoring 6-Feature Cross-Node Telemetry...")

try:
    while True:
        # 1. Real Hardware Telemetry (Node 10)
        cpu_10 = psutil.cpu_percent()
        power_10 = 60.0 + (cpu_10 * 0.1) 
        
        # 2. Simulated Network Telemetry (Nodes 8 & 6)
        cpu_8 = 25.0 
        latency_8 = 5.0
        latency_6 = 4.0
        selected_node = 10.0
        
        current_metrics = [power_10, cpu_10, cpu_8, latency_8, latency_6, selected_node]
        history_window.append(current_metrics)
        
        if len(history_window) > TIME_STEPS:
            history_window.pop(0)
            
            input_data = np.array(history_window)
            input_scaled = scaler.transform(input_data)
            input_reshaped = input_scaled.reshape(1, TIME_STEPS, 6) 
            
            pred_latency = model.predict(input_reshaped, verbose=0)[0][0]
            
            print(f"[MONITOR] Node10_CPU: {cpu_10}% | Node8_CPU: {cpu_8}% | Pred_Risk: {pred_latency:.4f}")
            
            if pred_latency > LATENCY_THRESHOLD:
                print("⚠️  [URLLC TRIGGER] Cross-Node Network Anomaly! Safety message dispatched!")
                sock.sendto(b"URLLC_EMERGENCY_REROUTE", (UDP_IP, UDP_PORT))
                
        time.sleep(1)

except KeyboardInterrupt:
    print("\nAdvanced Controller safely shut down.")