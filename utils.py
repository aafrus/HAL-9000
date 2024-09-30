# utils.py
import json
import os
from alarm import Alarm

ALARMS_FILE = 'alarms.json'

def load_alarms():
    alarms = []
    if os.path.exists(ALARMS_FILE):
        with open(ALARMS_FILE, 'r') as f:
            data = json.load(f)
            for item in data:
                alarm = Alarm(item['alarm_type'], item['threshold'])
                alarms.append(alarm)
        print("Laddar tidigare konfigurerade larm...")
    return alarms

def save_alarms(alarms):
    data = [{'alarm_type': alarm.alarm_type, 'threshold': alarm.threshold} for alarm in alarms]
    with open(ALARMS_FILE, 'w') as f:
        json.dump(data, f, indent=4)
