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