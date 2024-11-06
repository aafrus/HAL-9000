"""
System Resource Monitor
-------------------
Terminal-based application for monitoring system resources and managing alerts.

The application provides real-time monitoring of system resources (CPU, memory, 
disk usage) and configurable threshold-based alerts. Features a terminal UI
for system interaction and monitoring.

Components:
    - GUI: Terminal user interface
    - MonitoringSystem: Resource monitoring
    - AlarmManager: Alert configuration
    - Logger: Event logging
"""

import sys
import subprocess

#Checks Windows
if sys.platform == "win32":
    try:
        import curses
    except ImportError:
        print("Försöker installera windows-curses...")
        try:
            # Försök att installera windows-curses om det saknas
            subprocess.check_call([sys.executable, "-m", "pip", "install", "windows-curses"])
            import curses  # Försök att importera curses igen efter installation
        except subprocess.CalledProcessError as e:
            print(f"Misslyckades att installera windows-curses: {e}")
            sys.exit(1)

from gui import GUI
from monitoring import MonitoringSystem
from alarm_manager import AlarmManager
from logging_app import Logger

def main() -> None:
    """Initialize and run the monitoring application.
    
    Creates core system components and starts the user interface.
    Ensures proper cleanup and logging on exit.
    """
    logger = Logger()
    alarm_manager = AlarmManager(logger)
    monitoring_system = MonitoringSystem(logger)
    
    gui = GUI(alarm_manager, monitoring_system, logger)
    try:
        gui.run()
    finally:
        logger.log_event("Program_Ended")


if __name__ == "__main__":
    main()
