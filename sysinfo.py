# sysinfo.py
import psutil
import platform
import shutil
import time
import os

class SysInfoDisplay:
    def __init__(self):
        self.clear_screen()

    def clear_screen(self):
        os.system('cls' if platform.system() == 'Windows' else 'clear')

    def format_bar(self, value, total=100, size=20, bar_char="█", empty_char=" "):
        filled = int(size * value / total)
        return bar_char * filled + empty_char * (size - filled)

    def display_info(self):
        cpu_percent = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Draw system info
        print(f"User: {os.getlogin()}")
        print(f"System: {platform.system()} {platform.release()}")
        print(f"CPU Usage: {cpu_percent}%")
        print(f"Memory Usage: {mem.percent}% ({mem.used // (1024 ** 2)} MB used)")
        print(f"Disk Usage: {disk.percent}% ({disk.used // (1024 ** 3)} GB used)")

        print("\nResource Usage Bars:")
        print(f"CPU  [{self.format_bar(cpu_percent)}] {cpu_percent}%")
        print(f"RAM  [{self.format_bar(mem.percent)}] {mem.percent}%")
        print(f"Disk [{self.format_bar(disk.percent)}] {disk.percent}%")

        input("\nPress any key to return to menu...")