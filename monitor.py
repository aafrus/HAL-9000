# monitor.py
import psutil
import platform

class Monitor:
    def __init__(self):
        # Anpassa diskvägen beroende på operativsystem
        if platform.system() == 'Windows':
            self.disk_path = 'C:\\'
        else:
            self.disk_path = '/'

    def get_cpu_usage(self):
        # CPU-användning med 1 sekunders intervall
        return psutil.cpu_percent(interval=1)

    def get_memory_usage(self):
        # Hämtar minnesanvändning
        mem = psutil.virtual_memory()
        percent = mem.percent
        used = mem.used // (1024 ** 2)  # Omvandlar till MB
        total = mem.total // (1024 ** 2)
        return percent, used, total

    def get_disk_usage(self):
        # Hämtar diskanvändning baserat på operativsystemets diskväg
        disk = psutil.disk_usage(self.disk_path)
        percent = disk.percent
        used = disk.used // (1024 ** 3)  # Omvandlar till GB
        total = disk.total // (1024 ** 3)
        return percent, used, total