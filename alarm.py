# alarm.py
class Alarm:
    def __init__(self, alarm_type, threshold):
        self.alarm_type = alarm_type  # 'CPU', 'Memory', or 'Disk'
        self.threshold = threshold

    def __str__(self):
        return f"{self.alarm_type} larm {self.threshold}%"
