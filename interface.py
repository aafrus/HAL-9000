# interface.py

# Define ANSI escape sequences for colors
class Colors:
    BLK = "\033[30m"
    RED = "\033[31m"
    GRN = "\033[32m"
    YLW = "\033[33m"
    BLU = "\033[34m"
    PUR = "\033[35m"
    CYN = "\033[36m"
    WHT = "\033[37m"
    GRY = "\033[90;1m"
    RST = "\033[0m"
    BLD = "\033[1m"

# Function to format colored text
def colored_text(text, color, bold=False):
    if bold:
        return f"{Colors.BLD}{color}{text}{Colors.RST}"
    return f"{color}{text}{Colors.RST}"

# Padding/Alignment functions
def center_text(text, width):
    return text.center(width)

# Function to draw a colored header
def draw_header(name, host, uptime):
    header = f"""
{colored_text('user', Colors.YLW)} {colored_text(name, Colors.RED, bold=True)}
{colored_text('host', Colors.YLW)} {colored_text(host, Colors.GRN, bold=True)}
{colored_text('up', Colors.YLW)} {colored_text(uptime, Colors.CYN, bold=True)}
"""
    return header

def draw_progress_bar(percentage, size=15, color=Colors.PUR):
    full = '─'
    empty = '┄'
    filled_length = int(size * percentage // 100)
    bar = (f"{Colors.BLD}{color}{full * filled_length}"
           f"{Colors.GRY}{empty * (size - filled_length)}{Colors.RST}")
    return bar

# Example CPU and RAM display function
def display_cpu_ram(cpu, ram, width=34):
    cpu_bar = draw_progress_bar(cpu, color=Colors.PUR)
    ram_bar = draw_progress_bar(ram, color=Colors.PUR)
    
    output = f"{center_text('CPU', width)} {cpu}% {cpu_bar}\n"
    output += f"{center_text('RAM', width)} {ram}% {ram_bar}\n"
    return output

import sys

def get_cpu_usage():
    # Placeholder for actual CPU usage retrieval
    return 45  # Example value

def get_memory_usage():
    # Placeholder for actual memory usage retrieval
    return 70  # Example value

def display_info():
    cpu_usage = get_cpu_usage()
    mem_usage = get_memory_usage()

    sys.stdout.write(f"\r{colored_text('HAL-9000 System Monitor', Colors.YLW, bold=True)}\n")
    sys.stdout.write(f"\r{colored_text('CPU Usage:', Colors.BLU)} {cpu_usage}% {draw_progress_bar(cpu_usage, 15, Colors.RED)}\n")
    sys.stdout.write(f"\r{colored_text('Memory Usage:', Colors.BLU)} {mem_usage}% {draw_progress_bar(mem_usage, 15, Colors.GREEN)}\n")
    sys.stdout.flush()

# Testa funktionen
if __name__ == "__main__":
    display_info()
