import psutil
import time

def monitor_network_state(interface="WiFi", interval=1):
    print(f"--- Experiment 2: Real-time Network State Monitoring ---")
    print(f"Initializing sensor on interface: {interface}...\n")
    
    try:
        while True:
            # 1. Capture initial network hardware state
            net_io_1 = psutil.net_io_counters(pernic=True)
            
            if interface not in net_io_1:
                print(f"Error: Interface '{interface}' not found.")
                print(f"Available interfaces: {list(net_io_1.keys())}")
                break
                
            bytes_sent_1 = net_io_1[interface].bytes_sent
            bytes_recv_1 = net_io_1[interface].bytes_recv
            
            # 2. Wait for the defined time interval (1 second)
            time.sleep(interval)
            
            # 3. Capture secondary network hardware state
            net_io_2 = psutil.net_io_counters(pernic=True)
            bytes_sent_2 = net_io_2[interface].bytes_sent
            bytes_recv_2 = net_io_2[interface].bytes_recv
            
            # 4. Calculate the delta (throughput per second)
            sent_per_sec = bytes_sent_2 - bytes_sent_1
            recv_per_sec = bytes_recv_2 - bytes_recv_1
            
            # 5. Convert raw Bytes into Megabits per second (Mbps)
            sent_mbps = (sent_per_sec * 8) / 1_000_000
            recv_mbps = (recv_per_sec * 8) / 1_000_000
            
            # 6. Output the scientific metrics
            print(f"[METRIC] Throughput -> Sent: {sent_mbps:.2f} Mbps | Received: {recv_mbps:.2f} Mbps")
            
            # 7. Congestion Threshold Alert (Simulating eMBB interference)
            if recv_mbps > 15.0:
                print("[WARNING] Congestion Threshold Exceeded: High eMBB Traffic Detected!")

    except KeyboardInterrupt:
        print("\n--- Network State Monitoring Terminated ---")

if __name__ == "__main__":
    # If running on your Windows laptop, use "WiFi" or "Ethernet". 
    # If testing on the Pi later, change this to "wlan0" or "eth0".
    monitor_network_state(interface="WiFi", interval=1)