"""
Resource Monitoring Alarm System
-----------------------------
Manages threshold-based alerts for system resource utilization.
Handles creation, storage, and evaluation of CPU, memory, and disk usage alarms.
"""

from typing import List, Dict, Optional
import json
import os
from logging_app import Logger


class AlarmManager:
    """System resource alarm management service.
    
    Manages creation, persistence, and evaluation of resource usage alarms.
    Supports CPU, memory, and disk utilization thresholds.
    
    Attributes:
        alarms: Collection of configured resource alarms
        logger: Event logging service
    """

    def __init__(self, logger: Logger) -> None:
        """Initialize alarm system.
        
        Args:
            logger: Event logging service instance
        """
        self.alarms = []
        self.logger = logger
        self.load_alarms()
        
    def add_alarm(self, alarm_type: str, threshold: int) -> None:
        """Create and store new resource alarm.
        
        Args:
            alarm_type: Resource type to monitor
            threshold: Alert threshold percentage
        """
        self.alarms.append({
            "type": alarm_type,
            "threshold": threshold,
            "active": True
        })
        self.logger.log_event("Alarm_Created", {"type": alarm_type, "threshold": threshold})
        self.save_alarms()
        
    def remove_alarm(self, index: int) -> None:
        """Remove alarm configuration.
        
        Args:
            index: Position of alarm to remove
        """
        if 0 <= index < len(self.alarms):
            self.alarms.pop(index)
            self.logger.log_event("Alarm_Removed")
            self.save_alarms()
    
    def load_alarms(self) -> None:
        """Load alarm configurations from storage."""
        try:
            if os.path.exists('alarms.json'):
                with open('alarms.json', 'r') as f:
                    self.alarms = json.load(f)
            else:
                self.alarms = []
                self.save_alarms()
        except Exception as e:
            self.alarms = []
            self.save_alarms()
    
    def save_alarms(self) -> None:
        """Persist alarm configurations to storage."""
        try:
            with open('alarms.json', 'w') as f:
                json.dump(self.alarms, f, indent=4)
        except Exception as e:
            pass
    
    def check_alarms(self, cpu: Optional[float], memory: Optional[float], disk: Optional[float]) -> List[Dict]:
        """Evaluate resource metrics against alarm thresholds.
        
        Args:
            cpu: Current CPU utilization percentage
            memory: Current memory utilization percentage
            disk: Current disk utilization percentage
            
        Returns:
            List of triggered alarms
        """
        triggered = []
        
        for alarm in self.alarms:
            alarm_type = alarm['type'].upper()
            threshold = alarm['threshold']
            
            if alarm_type == 'CPU' and cpu and cpu >= threshold:
                triggered.append(alarm)
            elif alarm_type == 'MEMORY' and memory and memory >= threshold:
                triggered.append(alarm)
            elif alarm_type == 'DISK' and disk and disk >= threshold:
                triggered.append(alarm)
        
        return triggered
    
    def get_alarms(self) -> List[Dict]:
        """Retrieve sorted list of configured alarms.
        
        Returns:
            List of alarms sorted by resource type
        """
        return sorted(self.alarms, key=lambda x: x['type'].upper())