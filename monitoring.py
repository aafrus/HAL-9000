"""
System Resource Monitor
---------------------
Core module for system resource monitoring and data collection.
Provides tracking of CPU, memory, and disk usage with historical data retention.
"""

import psutil
from typing import Optional, Tuple, List, Dict
from threading import Thread


class MonitoringSystem:
    """System resource monitoring and data collection service.
    
    Tracks and stores system resource usage including CPU, memory, and disk utilization.
    Supports real-time monitoring, historical data collection, and alarm triggers.
    
    Attributes:
        logger: Logging service for system events
        monitoring_active: Status of monitoring service
        monitoring_thread: Background monitoring process
        cpu_usage: CPU utilization history
        memory_usage: Memory utilization history
        disk_usage: Disk utilization history
    """

    MAX_HISTORY = 1000

    def __init__(self, logger=None) -> None:
        """Initialize the monitoring system.

        Args:
            logger: Event logging service instance
        """
        self.logger = logger
        self.monitoring_active = False
        self.monitoring_thread = None
        self.cpu_usage: List[float] = []
        self.memory_usage: List[float] = []
        self.disk_usage: List[float] = []

    def start_monitoring(self) -> None:
        """Start system resource monitoring."""
        self.monitoring_active = True
        if self.logger:
            self.logger.log_event("Monitoring_Started")

    def stop_monitoring(self) -> None:
        """Stop system resource monitoring."""
        self.monitoring_active = False
        if self.logger:
            self.logger.log_event("Monitoring_Stopped")

    def shutdown(self) -> None:
        """Perform clean system shutdown."""
        self.stop_monitoring()

    def get_cpu_usage(self) -> Optional[float]:
        """Get current CPU utilization percentage.

        Returns:
            Current CPU usage or None if monitoring inactive
        """
        if not self.monitoring_active:
            return None
        
        usage = psutil.cpu_percent(interval=1)
        self.cpu_usage.append(usage)
        if len(self.cpu_usage) > self.MAX_HISTORY:
            self.cpu_usage = self.cpu_usage[-self.MAX_HISTORY:]
        return usage

    def get_memory_usage(self) -> Optional[float]:
        """Get current memory utilization percentage.

        Returns:
            Current memory usage or None if monitoring inactive
        """
        if not self.monitoring_active:
            return None
        
        usage = psutil.virtual_memory().percent
        self.memory_usage.append(usage)
        if len(self.memory_usage) > self.MAX_HISTORY:
            self.memory_usage = self.memory_usage[-self.MAX_HISTORY:]
        return usage

    def get_disk_usage(self) -> Optional[float]:
        """Get current disk utilization percentage.

        Returns:
            Current disk usage or None if monitoring inactive
        """
        if not self.monitoring_active:
            return None
        
        usage = psutil.disk_usage('/').percent
        self.disk_usage.append(usage)
        if len(self.disk_usage) > self.MAX_HISTORY:
            self.disk_usage = self.disk_usage[-self.MAX_HISTORY:]
        return usage

    def get_memory_details(self) -> Optional[Tuple[float, float, float]]:
        """Get detailed memory statistics.

        Returns:
            Tuple of (used_gb, total_gb, usage_percentage) or None if inactive
        """
        if not self.monitoring_active:
            return None
        
        memory = psutil.virtual_memory()
        used_gb = memory.used / (1024 ** 3)
        total_gb = memory.total / (1024 ** 3)
        return used_gb, total_gb, memory.percent

    def get_disk_details(self) -> Optional[Tuple[float, float, float]]:
        """Get detailed disk statistics.

        Returns:
            Tuple of (used_gb, total_gb, usage_percentage) or None if inactive
        """
        if not self.monitoring_active:
            return None
        
        disk = psutil.disk_usage('/')
        used_gb = disk.used / (1024 ** 3)
        total_gb = disk.total / (1024 ** 3)
        return used_gb, total_gb, disk.percent

    def get_alarm_data(self) -> Tuple[Optional[float], Optional[float], Optional[float]]:
        """Retrieve current system metrics for alarm evaluation.

        Returns:
            Tuple of (cpu_usage, memory_usage, disk_usage) percentages
        """
        if not self.monitoring_active:
            self.logger.log_event("Monitoring_Data_Request_Failed", {"reason": "Monitoring not active"})
            return None, None, None
        
        try:
            cpu = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/').percent
            
            self.logger.log_event("System_Values_Retrieved", {
                "cpu": cpu,
                "memory": memory,
                "disk": disk
            })
            
            return cpu, memory, disk
        except Exception as e:
            self.logger.log_event("System_Values_Error", {"error": str(e)})
            return None, None, None

    def get_live_data(self) -> Tuple[Optional[float], Optional[float], Optional[float]]:
        """Retrieve current system resource utilization stats.

        Returns:
            Tuple of (cpu_usage, memory_usage, disk_usage) percentages
            Returns None values if monitoring inactive or on error
        """
        if not self.monitoring_active:
            return None, None, None
        
        try:
            cpu = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/').percent
            
            self.cpu_usage.append(cpu)
            self.memory_usage.append(memory)
            self.disk_usage.append(disk)
            
            if len(self.cpu_usage) > self.MAX_HISTORY:
                self.cpu_usage = self.cpu_usage[-self.MAX_HISTORY:]
            if len(self.memory_usage) > self.MAX_HISTORY:
                self.memory_usage = self.memory_usage[-self.MAX_HISTORY:]
            if len(self.disk_usage) > self.MAX_HISTORY:
                self.disk_usage = self.disk_usage[-self.MAX_HISTORY:]
                
            return cpu, memory, disk
        except Exception as e:
            if self.logger:
                self.logger.log_event("Monitoring_Error", {"error": str(e)})
            return None, None, None