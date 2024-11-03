"""
Event Logging System
------------------
Provides structured event logging functionality for system monitoring.
Records system events, state changes, and monitoring activities to timestamped log files.
"""

from datetime import datetime
import os


class Logger:
    """Event logging service for system monitoring.
    
    Manages structured logging of system events to timestamped files.
    Supports various event types including system state changes,
    monitoring activities, and alarm events.
    
    Attributes:
        log_file: File path for event logs
        allowed_events: Valid event types for logging
    """
    
    allowed_events = {
        "Program_Started",
        "Program_Ended",
        "Program_Ended_By_User",
        "Monitoring_Started",
        "Monitoring_Stopped",
        "Displaying_Active_Monitoring",
        "Displaying_Alarms",
        "Monitoring_Interface_Started",
        "System_Values_Retrieved",
        "Alarm_Created",
        "Alarm_Removed",
        "Alarm_Triggered"
    }

    def __init__(self) -> None:
        """Initialize logging service with timestamped file."""
        os.makedirs("logs", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = f"logs/log_{timestamp}.log"

    def log_event(self, event_type: str, data: dict = None) -> None:
        """Record a system event with timestamp.
        
        Args:
            event_type: Type of event to log
            data: Optional additional event data
        """
        timestamp = datetime.now().strftime("%d/%m/%Y_%H:%M")
        
        match event_type:
            case "Program_Started":
                log_entry = f"{timestamp}_Program_Started"
            case "Program_Ended":
                log_entry = f"{timestamp}_Program_Ended"
            case "Program_Ended_By_User":
                log_entry = f"{timestamp}_Program_Ended_By_User"
            case "Monitoring_Started":
                log_entry = f"{timestamp}_Monitoring_Started"
            case "Monitoring_Stopped":
                log_entry = f"{timestamp}_Monitoring_Stopped"
            case "Displaying_Active_Monitoring":
                log_entry = f"{timestamp}_Displaying_Active_Monitoring"
            case "Displaying_Alarms":
                log_entry = f"{timestamp}_Displaying_Alarms"
            case "Monitoring_Interface_Started":
                log_entry = f"{timestamp}_Monitoring_Interface_Started"
            case "System_Values_Retrieved":
                log_entry = f"{timestamp}_System_Values_Retrieved"
            case "Alarm_Created" if data:
                log_entry = f"{timestamp}_Alarm_Created_{data['type']}_{data['threshold']}_Percent"
            case "Alarm_Removed" if data:
                log_entry = f"{timestamp}_Alarm_Removed"
            case "Alarm_Triggered" if data:
                log_entry = f"{timestamp}_Alarm_Triggered_{data['type']}_{data['threshold']}_Percent"
            case _:
                log_entry = f"{timestamp}_{event_type}"
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry + '\n')