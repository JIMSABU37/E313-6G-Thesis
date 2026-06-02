import multiprocessing

def burn_core():
    while True:
        # Meaningless math to keep the CPU working at maximum speed
        x = 1000 * 1000 

if __name__ == '__main__':
    cores = multiprocessing.cpu_count()
    print(f"🔥 Starting stress test on all {cores} CPU cores! Press Ctrl+C to stop. 🔥")
    processes = []

    for i in range(cores):
        p = multiprocessing.Process(target=burn_core)
        p.start()
        processes.append(p)

    try:
        for p in processes:
            p.join()
    except KeyboardInterrupt:
        for p in processes:
            p.terminate()
        print("\nStress test stopped. CPU returning to normal.")
