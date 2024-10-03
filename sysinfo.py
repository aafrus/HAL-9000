#interface.py
import os
import time

# ANSI color codes
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"
WHITE = "\033[37m"
RESET = "\033[0m"
BOLD = "\033[1m"
GRAY = "\033[90m"
FULL = "─"
EMPTY = "┄"

def draw_progress(perc, size, color):
    inc = int(perc * size / 100)
    bar = (FULL * inc).ljust(size, EMPTY)
    return f"{color}{bar}{RESET}"

def get_cpu_usage():
    # Simulating CPU usage for the example
    return os.getloadavg()[0] * 10  # Convert loadavg to percentage

def get_memory_usage():
    # Simulate memory usage in percentage
    total_memory = 8000  # Example total memory in MB
    used_memory = 4000  # Example used memory in MB
    return int(used_memory / total_memory * 100)

def display_info():
    cpu_usage = get_cpu_usage()
    mem_usage = get_memory_usage()

    print(f"{YELLOW}  HAL-9000 System Monitor{RESET}")
    print(f"{BLUE}  CPU Usage:  {cpu_usage}% {draw_progress(cpu_usage, 15, RED)}")
    print(f"{BLUE}  Memory Usage: {mem_usage}% {draw_progress(mem_usage, 15, GREEN)}")

if __name__ == "__main__":
    while True:
        os.system('clear')  # Clear the terminal
        display_info()
        time.sleep(5)  # Refresh every 5 seconds
