# main.py
from monitor import Monitor
from alarm import Alarm
from logger import setup_logger, log_event
from utils import load_alarms, save_alarms
from emailsender import send_email
import threading
import time
import sys

def main():
    setup_logger()
    monitor = Monitor()
    alarms = load_alarms()
    active_monitoring = False
    monitoring_thread = None

    def start_monitoring():
        nonlocal active_monitoring, monitoring_thread
        active_monitoring = True
        print("Övervakning startad.")
        log_event("Övervakning_startad")

        def monitor_loop():
            while active_monitoring:
                cpu_usage = monitor.get_cpu_usage()
                mem_usage, mem_used, mem_total = monitor.get_memory_usage()
                disk_usage, disk_used, disk_total = monitor.get_disk_usage()

                check_alarms('CPU', cpu_usage)
                check_alarms('Memory', mem_usage)
                check_alarms('Disk', disk_usage)

                time.sleep(1)

        monitoring_thread = threading.Thread(target=monitor_loop)
        monitoring_thread.start()

    def stop_monitoring():
        nonlocal active_monitoring
        active_monitoring = False
        if monitoring_thread:
            monitoring_thread.join()
        print("Övervakning stoppad.")
        log_event("Övervakning_stoppad")

    def check_alarms(alarm_type, value):
        relevant_alarms = [alarm for alarm in alarms if alarm.alarm_type == alarm_type]
        if not relevant_alarms:
            return

        thresholds = [alarm.threshold for alarm in relevant_alarms]
        thresholds.sort(reverse=True)
        for threshold in thresholds:
            if value >= threshold:
                message = f"***VARNING, LARM AKTIVERAT, {alarm_type.upper()} ANVÄNDNING ÖVERSTIGER {threshold}%***"
                print(message)
                log_event(f"{alarm_type}_Användningslarm_aktiverat_{threshold}_Procent")
                send_email(
                    subject=f"Larm: {alarm_type} användning över {threshold}%",
                    content=message
                )
                break  # Aktivera endast det högsta larmet

    def monitoring_mode():
        global active_monitoring
        active_monitoring = True  # Sätta övervakningen som aktiv
        print("Övervakning är aktiv. Tryck på Enter för att återgå till menyn.")

        # Starta en separat tråd för att hantera statusutskriften
        def print_status():
            while active_monitoring:
                print("Övervakning är fortfarande aktiv...")
                time.sleep(5)  # Vänta i 5 sekunder innan nästa meddelande

        status_thread = threading.Thread(target=print_status)
        status_thread.start()

        # Vänta på Enter för att stoppa övervakningen
        input()  # Väntar på att användaren trycker Enter
        active_monitoring = False  # Avsluta övervakning
        status_thread.join()  # Vänta på att status-tråden ska avslutas
        print("\nÅtergår till huvudmenyn.")
        log_event("Övervakningsläge_stoppat")

    while True:
        print("\nVälj ett alternativ:")
        print("1. Starta övervakning")
        print("2. Lista aktiv övervakning")
        print("3. Skapa larm")
        print("4. Visa larm")
        print("5. Ta bort larm")
        print("6. Starta övervakningsläge")
        print("7. Avsluta")

        choice = input("Ange ditt val: ")
        if choice == '1':
            start_monitoring()
        elif choice == '2':
            if not active_monitoring:
                print("Ingen övervakning är aktiv.")
            else:
                cpu_usage = monitor.get_cpu_usage()
                mem_usage, mem_used, mem_total = monitor.get_memory_usage()
                disk_usage, disk_used, disk_total = monitor.get_disk_usage()
                print(f"CPU Användning: {cpu_usage}%")
                print(f"Minnesanvändning: {mem_usage}% ({mem_used} MB av {mem_total} MB används)")
                print(f"Diskanvändning: {disk_usage}% ({disk_used} GB av {disk_total} GB används)")
            input("Tryck valfri tangent för att gå tillbaka till huvudmeny.")
        elif choice == '3':
            print("\nKonfigurera larm:")
            print("1. CPU användning")
            print("2. Minnesanvändning")
            print("3. Diskanvändning")
            print("4. Tillbaka till huvudmeny")
            alarm_choice = input("Ange ditt val: ")
            if alarm_choice in ['1', '2', '3']:
                alarm_types = {'1': 'CPU', '2': 'Memory', '3': 'Disk'}
                alarm_type = alarm_types[alarm_choice]
                try:
                    level = int(input("Ställ in nivå för alarm mellan 1-100: "))
                    if 1 <= level <= 100:
                        new_alarm = Alarm(alarm_type, level)
                        alarms.append(new_alarm)
                        save_alarms(alarms)
                        print(f"Larm för {alarm_type} användning satt till {level}%.")
                        log_event(f"{alarm_type}_Användningslarm_Konfigurerat_{level}_Procent")
                    else:
                        print("Fel: Nivån måste vara mellan 1 och 100.")
                except ValueError:
                    print("Fel: Ogiltig inmatning, vänligen ange en siffra mellan 1 och 100.")
            elif alarm_choice == '4':
                continue
            else:
                print("Fel: Ogiltigt val.")
        elif choice == '4':
            if not alarms:
                print("Inga konfigurerade larm.")
            else:
                sorted_alarms = sorted(alarms, key=lambda x: x.alarm_type)
                for alarm in sorted_alarms:
                    print(alarm)
            input("Tryck valfri tangent för att gå tillbaka till huvudmeny.")
        elif choice == '5':
            if not alarms:
                print("Inga larm att ta bort.")
            else:
                print("Välj ett konfigurerat larm att ta bort:")
                for idx, alarm in enumerate(alarms, start=1):
                    print(f"{idx}. {alarm}")
                try:
                    alarm_idx = int(input("Ange numret på larmet att ta bort: "))
                    if 1 <= alarm_idx <= len(alarms):
                        removed_alarm = alarms.pop(alarm_idx - 1)
                        save_alarms(alarms)
                        print(f"Larm borttaget: {removed_alarm}")
                        log_event(f"{removed_alarm.alarm_type}_Användningslarm_Borttaget_{removed_alarm.threshold}_Procent")
                    else:
                        print("Fel: Ogiltigt nummer.")
                except ValueError:
                    print("Fel: Ogiltig inmatning, vänligen ange ett nummer.")
        elif choice == '6':
            print("Startar övervakningsläge...")
            log_event("Övervakningsläge_startat")
            monitoring_thread = threading.Thread(target=monitoring_mode)
            monitoring_thread.start()
            monitoring_thread.join()  # Vänta på att tråden ska sluta innan vi återgår till menyn
        elif choice == '7':
            if active_monitoring:
                stop_monitoring()
            print("Avslutar programmet.")
            sys.exit()
        else:
            print("Fel: Ogiltigt val.")

if __name__ == "__main__":
    main()

# main.py
from interface import draw_header, display_cpu_ram, colored_text

def main():
    name = "YourUsername"
    host = "YourHost"
    uptime = "1h 2m"
    cpu_usage = 75  # Example CPU usage
    ram_usage = 65  # Example RAM usage

    # Display header
    header = draw_header(name, host, uptime)
    print(header)

    # Display CPU and RAM usage
    usage_display = display_cpu_ram(cpu_usage, ram_usage)
    print(usage_display)

if __name__ == "__main__":
    main()
    