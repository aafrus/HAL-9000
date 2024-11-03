"""
GUI module
----------
Handles the terminal-based user interface for system monitoring.
The module uses curses to create an interactive terminal-based interface
that enables system monitoring and alarm management.
"""

import curses
import time
from datetime import datetime
from monitoring import MonitoringSystem
from alarm_manager import AlarmManager
from logging_app import Logger
from typing import Optional


class GUI:
    """
    Handles the graphical user interface in the terminal.
    
    Attributes:
        alarm_manager: Instance of the alarm manager
        monitoring_system: Instance of the monitoring system
        logger: Instance of the logger
        current_selection: Current menu selection
        menu_items: List of menu options
    """

    def __init__(self, alarm_manager, monitoring_system, logger) -> None:
        """
        Initializes GUI with necessary components.

        Args:
            alarm_manager: Instance of the alarm manager
            monitoring_system: Instance of the monitoring system
            logger: Instance of the logger
        """
        self.alarm_manager = alarm_manager
        self.monitoring_system = monitoring_system
        self.logger = logger
        self.current_selection = 0
        self.menu_items = [
            "1. Start System Monitoring",
            "2. Show System Status",
            "3. Create Alarm",
            "4. Show Alarms",
            "5. Remove Alarm",
            "6. Start Alarm Monitoring",
            "0. Exit"
        ]
        self.logger.log_event("Program_Started")

    def show_startup_message(self) -> None:
        """
        Displays startup message when the program initializes.
        """
        height, width = self.stdscr.getmaxyx()
        
        self.stdscr.clear()
        self.draw_border(self.stdscr, include_title=True)
        
        message = "Loading previously configured alarms..."
        self.center_text(self.stdscr, height//2-2, message)
        self.stdscr.refresh()
        curses.napms(1500)

    def create_progress_bar(self, value, total=100, length=20) -> str:
        """
        Creates a graphical progress indicator.

        Args:
            value: Current value to display (None or numeric)
            total: Maximum value for the progress indicator
            length: Desired length of the progress indicator

        Returns:
            str: Formatted progress indicator with filled and empty segments
        """
        if value is None:
            value = 0
        
        filled = int((float(value) / total) * length)
        if value >= 90:
            bar = "█" * filled + "░" * (length - filled)
            return f"[{bar}]"
        elif value >= 75:
            bar = "█" * filled + "░" * (length - filled)
            return f"[{bar}]"
        else:
            bar = "█" * filled + "░" * (length - filled)
            return f"[{bar}]"

    def center_text(self, window, y: int, text: str) -> None:
        """
        Centers text horizontally in a window.

        Args:
            window: Curses window to write to
            y: Vertical position for the text
            text: Text to center and display
        """
        height, width = window.getmaxyx()
        x = (width - len(text)) // 2
        try:
            window.addstr(y, x, text)
        except curses.error:
            pass

    def show_message(self, window, message: str, duration: float = 1.5) -> None:
        """
        Displays a temporary message in the window.

        Args:
            window: Curses window to display the message in
            message: Message to display
            duration: How long the message should be displayed in seconds
        """
        height, width = window.getmaxyx()
        y = height // 2
        self.center_text(window, y, message)
        window.refresh()
        curses.napms(int(duration * 1000))

    def init_curses(self) -> None:
        """
        Initializes curses with all necessary settings.
        Sets up color pairs and basic terminal settings.
        """
        self.stdscr = curses.initscr()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)   # Normal text
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)   # Selected object
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)     # Warnings
        curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)   # Confirmations
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.stdscr.keypad(True)

    def cleanup_curses(self) -> None:
        """
        Resets terminal settings and exits curses.
        Logs program exit.
        """
        self.logger.log_event("Program_Ended")
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    def show_confirmation(self, message: str, duration: float = 1) -> None:
        """
        Displays a confirmation message for a given duration.

        Args:
            message: Message to display
            duration: Duration of the display in seconds
        """
        height, width = self.stdscr.getmaxyx()
        confirm_win = curses.newwin(3, width - 4, height // 2, 2)
        confirm_win.clear()
        confirm_win.addstr(1, (width - len(message) - 4) // 2, message)
        confirm_win.refresh()
        curses.napms(duration * 1000)

    def draw_border(self, window, include_title: bool = False) -> None:
        """
        Draws a border around the window with an optional title.

        Args:
            window: Curses window to draw the border in
            include_title: If True, include the HAL-9000 title in the border
        """
        height, width = window.getmaxyx()
        last_line_length = width - 1
        
        try:
            window.addstr(0, 0, "─" * (last_line_length - 1))
            window.addstr(height-1, 0, "─" * (last_line_length - 1))
            
            for y in range(1, height-1):
                window.addstr(y, 0, "│")
                window.addstr(y, last_line_length - 1, "│")
            
            window.addstr(0, 0, "┌")
            window.addstr(0, last_line_length - 1, "┐")
            window.addstr(height-1, 0, "└")
            window.addstr(height-1, last_line_length - 1, "┘")
            
            if include_title:
                title = "─ HAL-9000 ─"
                title_pos = (width - len(title)) // 2
                window.addstr(0, title_pos, title)
                
        except curses.error:
            pass

    def draw_menu(self) -> None:
        """
        Draws the main menu with all menu options.
        Highlights the selected option with green color.
        """
        self.stdscr.clear()
        self.draw_border(self.stdscr, include_title=True)
        height, width = self.stdscr.getmaxyx()
        
        menu_start_y = (height - len(self.menu_items)) // 2
        
        for idx, item in enumerate(self.menu_items):
            x = (width - len(item)) // 2
            y = menu_start_y + idx
            
            if idx == self.current_selection:
                self.stdscr.attron(curses.color_pair(2))  # Green for selected
                self.center_text(self.stdscr, y, item)
                self.stdscr.attroff(curses.color_pair(2))
            elif idx == 0 and self.monitoring_system.monitoring_active:
                self.stdscr.attron(curses.color_pair(3))  # Red for active monitoring
                self.center_text(self.stdscr, y, item)
                self.stdscr.attroff(curses.color_pair(3))
            else:
                self.center_text(self.stdscr, y, item)
            
        self.stdscr.refresh()

    def show_monitoring_data(self) -> None:
        """
        Displays live system monitoring data with graphical progress indicators.
        Updates continuously until the user presses 'q'.
        """
        if not self.monitoring_system.monitoring_active:
            height, width = self.stdscr.getmaxyx()
            self.stdscr.clear()
            self.draw_border(self.stdscr, include_title=True)
            self.center_text(self.stdscr, height//2-2, "No active monitoring")
            self.center_text(self.stdscr, height//2, "Press any key to return")
            self.stdscr.refresh()
            self.stdscr.getch()
            return

        self.stdscr.nodelay(1)
        
        try:
            while True:
                self.stdscr.clear()
                self.draw_border(self.stdscr, include_title=True)
                height, width = self.stdscr.getmaxyx()
                
                cpu, memory, disk = self.monitoring_system.get_live_data()
                
                if cpu is None or memory is None or disk is None:
                    break
                
                start_y = height // 2 - 2
                
                cpu_bar = self.create_progress_bar(cpu)
                mem_bar = self.create_progress_bar(memory)
                disk_bar = self.create_progress_bar(disk)
                
                cpu_text = f"CPU Usage    | {cpu:5.1f}% {cpu_bar}"
                mem_text = f"Memory Usage | {memory:5.1f}% {mem_bar}"
                disk_text = f"Disk Usage   | {disk:5.1f}% {disk_bar}"
                
                self.center_text(self.stdscr, start_y, cpu_text)
                self.center_text(self.stdscr, start_y + 2, mem_text)
                self.center_text(self.stdscr, start_y + 4, disk_text)
                
                self.center_text(self.stdscr, height-3, "Press 'q' to return to menu")
                
                self.stdscr.refresh()
                
                try:
                    key = self.stdscr.getch()
                    if key == ord('q'):
                        break
                except curses.error:
                    pass
                
                curses.napms(100)
                
        finally:
            self.stdscr.nodelay(0)

    def show_monitoring_interface(self) -> None:
        """
        Shows the alarm monitoring interface with real-time alerts.
        """
        if not self.monitoring_system.monitoring_active:
            height, width = self.stdscr.getmaxyx()
            self.stdscr.clear()
            self.draw_border(self.stdscr, include_title=True)
            self.center_text(self.stdscr, height//2-2, "No active monitoring")
            self.center_text(self.stdscr, height//2, "Press 'q' to return")
            self.stdscr.refresh()
            self.stdscr.getch()
            return

        height, width = self.stdscr.getmaxyx()
        warning_history = []
        last_check = time.time()
        check_interval = 5
        
        self.stdscr.nodelay(1)
        
        try:
            while True:
                current_time = time.time()
                if current_time - last_check >= check_interval:
                    cpu, memory, disk = self.monitoring_system.get_alarm_data()
                    triggered_alarms = self.alarm_manager.check_alarms(cpu, memory, disk)
                    
                    if triggered_alarms:
                        timestamp = datetime.now().strftime("[%H:%M:%S]")
                        for alarm in triggered_alarms:
                            warning = f"{timestamp} ***WARNING! {alarm['type']} USAGE EXCEEDS {alarm['threshold']}%***"
                            if warning not in warning_history:
                                warning_history.insert(0, warning)
                        warning_history = warning_history[:8]  # Keep last 8 warnings
                    last_check = current_time

                self.stdscr.clear()
                self.draw_border(self.stdscr, include_title=True)
                
                # Show monitoring status
                self.stdscr.attron(curses.color_pair(1))
                self.center_text(self.stdscr, 3, "MONITORING ACTIVE")
                self.stdscr.attroff(curses.color_pair(1))
                
                # Show warnings
                warning_y = 5
                if warning_history:
                    for warning in warning_history:
                        self.stdscr.attron(curses.color_pair(1))
                        self.center_text(self.stdscr, warning_y, warning)
                        self.stdscr.attroff(curses.color_pair(1))
                        warning_y += 1

                self.center_text(self.stdscr, height-3, "Press 'q' to return to menu")
                self.stdscr.refresh()

                try:
                    key = self.stdscr.getch()
                    if key == ord('q'):
                        break
                except curses.error:
                    pass
                
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            pass
        finally:
            self.stdscr.nodelay(0)

    def show_create_alarm_menu(self) -> None:
        """
        Display menu for creating new alarms with arrow key navigation.
        """
        alarm_types = ["1. Create CPU Alarm", "2. Create Memory Alarm", "3. Create Disk Alarm"]
        current_selection = 0
        
        while True:
            self.stdscr.clear()
            height, width = self.stdscr.getmaxyx()
            self.draw_border(self.stdscr, include_title=True)
            
            # Draw menu items
            start_y = height // 2 - len(alarm_types) // 2
            for idx, menu_text in enumerate(alarm_types):
                if idx == current_selection:
                    self.stdscr.attron(curses.color_pair(2))  # Green for selected
                    self.center_text(self.stdscr, start_y + idx, menu_text)
                    self.stdscr.attroff(curses.color_pair(2))
                else:
                    self.center_text(self.stdscr, start_y + idx, menu_text)
            
            self.center_text(self.stdscr, height-3, "Use arrow keys to select, Enter to confirm, ESC to cancel")
            self.stdscr.refresh()
            
            # Handle key input
            key = self.stdscr.getch()
            if key == curses.KEY_UP and current_selection > 0:
                current_selection -= 1
            elif key == curses.KEY_DOWN and current_selection < len(alarm_types) - 1:
                current_selection += 1
            elif key == 10:  # Enter key
                alarm_type = ["cpu", "memory", "disk"][current_selection]
                self.create_alarm(alarm_type)
                break
            elif key == 27:  # Escape key
                break

    def create_alarm(self, alarm_type: str) -> None:
        """
        Create a new alarm with the specified type and threshold.
        """
        height, width = self.stdscr.getmaxyx()
        self.stdscr.clear()
        self.draw_border(self.stdscr, include_title=True)
        
        self.center_text(self.stdscr, height//2-2, f"Enter threshold for {alarm_type} alarm (1-100):")
        self.center_text(self.stdscr, height//2, "")
        self.stdscr.refresh()
        
        # Get threshold input
        curses.echo()
        threshold_str = self.stdscr.getstr(height//2, width//2-2, 3).decode('utf-8')
        curses.noecho()
        
        try:
            threshold = int(threshold_str)
            if 1 <= threshold <= 100:
                self.alarm_manager.add_alarm(alarm_type, threshold)
                self.center_text(self.stdscr, height//2+2, "Alarm created successfully!")
            else:
                self.center_text(self.stdscr, height//2+2, "Invalid threshold! Must be between 1 and 100.")
        except ValueError:
            self.center_text(self.stdscr, height//2+2, "Invalid input! Please enter a number.")
        
        self.stdscr.refresh()
        time.sleep(2)

    def show_alarms(self) -> None:
        """
        Display all configured alarms in a sorted list.
        """
        height, width = self.stdscr.getmaxyx()
        self.stdscr.clear()
        self.draw_border(self.stdscr, include_title=True)

        if not self.alarm_manager.alarms:
            self.center_text(self.stdscr, height//2, "No alarms configured")
            self.center_text(self.stdscr, height//2 + 2, "Press any key to return to menu")
            self.stdscr.refresh()
            self.stdscr.getch()
            return

        # Sortera larmen efter typ och tröskelvärde
        sorted_alarms = sorted(self.alarm_manager.alarms, key=lambda x: (x['type'], x['threshold']))
        
        # Visa rubrik
        self.center_text(self.stdscr, 2, "Configured alarms:")
        
        # Visa larmen
        for i, alarm in enumerate(sorted_alarms, 1):
            alarm_text = f"{i}. {alarm['type']} Usage > {alarm['threshold']}%"
            self.center_text(self.stdscr, 3 + i, alarm_text)

        self.center_text(self.stdscr, height-3, "Press any key to return to menu")
        self.stdscr.refresh()
        self.stdscr.getch()

    def remove_alarm(self) -> None:
        """
        Show the remove alarm interface with arrow navigation.
        """
        alarms = self.alarm_manager.get_alarms()
        if not alarms:
            height, width = self.stdscr.getmaxyx()
            self.stdscr.clear()
            self.draw_border(self.stdscr, include_title=True)
            self.center_text(self.stdscr, height//2-2, "No alarms configured")
            self.center_text(self.stdscr, height//2, "Press any key to return")
            self.stdscr.refresh()
            self.stdscr.getch()
            return

        current_selection = 0
        while True:
            height, width = self.stdscr.getmaxyx()
            self.stdscr.clear()
            self.draw_border(self.stdscr, include_title=True)
            
            # Header
            self.center_text(self.stdscr, 2, "Current Alarms:")
            
            # Display alarms
            for i, alarm in enumerate(alarms):
                if i == current_selection:
                    self.stdscr.attron(curses.color_pair(2))
                    self.center_text(self.stdscr, 4+i, f"> {str(i+1).rjust(2)}. {alarm['type']} > {alarm['threshold']}%")
                    self.stdscr.attroff(curses.color_pair(2))
                else:
                    self.center_text(self.stdscr, 4+i, f"  {str(i+1).rjust(2)}. {alarm['type']} > {alarm['threshold']}%")

            # Footer
            self.center_text(self.stdscr, height-3, "Use ↑↓ to select, Enter to remove, 'q' to return")
            self.stdscr.refresh()

            # Handle input
            key = self.stdscr.getch()
            if key == curses.KEY_UP and current_selection > 0:
                current_selection -= 1
            elif key == curses.KEY_DOWN and current_selection < len(alarms) - 1:
                current_selection += 1
            elif key == ord('\n'):  # Enter key
                # Show confirmation message
                self.stdscr.clear()
                self.draw_border(self.stdscr, include_title=True)
                self.center_text(self.stdscr, height//2-2, f"Alarm removed: {alarms[current_selection]['type']} > {alarms[current_selection]['threshold']}%")
                self.center_text(self.stdscr, height//2, "Press any key to continue")
                self.stdscr.refresh()
                
                # Remove alarm and wait for key press
                self.alarm_manager.remove_alarm(current_selection)
                self.stdscr.getch()
                return
            elif key == ord('q'):
                return

    def run(self) -> None:
        """
        Huvudloop för applikationen.
        Hanterar menynavigering och användarinteraktion.
        """
        try:
            self.init_curses()
            self.show_startup_message()
            
            while True:
                try:
                    self.draw_menu()
                    key = self.stdscr.getch()
                    
                    if key in [curses.KEY_UP, ord('k')] and self.current_selection > 0:
                        self.current_selection -= 1
                    elif key in [curses.KEY_DOWN, ord('j')] and self.current_selection < len(self.menu_items) - 1:
                        self.current_selection += 1
                    elif key in [curses.KEY_ENTER, ord('\n'), ord(' ')]:
                        if self.current_selection == 0:  # Start Monitoring
                            self.monitoring_system.start_monitoring()
                            self.logger.log_event("Monitoring_Started")
                            self.show_confirmation("Monitoring started!")
                        elif self.current_selection == 1:  # List Active Monitoring
                            self.logger.log_event("Displaying_Active_Monitoring")
                            self.show_monitoring_data()
                        elif self.current_selection == 2:  # Create Alarm
                            self.logger.log_event("Creating_Alarm")
                            self.show_create_alarm_menu()
                        elif self.current_selection == 3:  # Show Alarms
                            self.logger.log_event("Displaying_Alarms")
                            self.show_alarms()
                        elif self.current_selection == 4:  # Remove Alarm
                            self.logger.log_event("Removing_Alarm")
                            self.remove_alarm()
                        elif self.current_selection == 5:  # Start Monitoring Interface
                            self.logger.log_event("Monitoring_Interface_Started")
                            self.show_monitoring_interface()
                        elif self.current_selection == 6:  # Exit
                            self.logger.log_event("Program_Ended_By_User")
                            break
                    elif key in [ord('0'), ord('1'), ord('2'), ord('3'), ord('4'), ord('5'), ord('6')]:
                        self.current_selection = int(chr(key))
                        if self.current_selection == 0:
                            self.logger.log_event("Program_Ended_With_Digit")
                            break
                        self.current_selection -= 1
                    
                    elif key == ord('q'):
                        self.logger.log_event("Program_Ended_With_Q")
                        break
                        
                except KeyboardInterrupt:
                    # Hantera Ctrl+C genom att avsluta programmet snyggt
                    self.logger.log_event("Program_Interrupted")
                    break
                except curses.error:
                    continue
                
        finally:
            self.cleanup_curses()


def main() -> None:
    """
    Starts the application and initializes all necessary modules.
    Creates instances of logger, alarm manager, and monitoring system
    and starts the user interface.
    """
    logger = Logger()
    alarm_manager = AlarmManager(logger)
    monitoring_system = MonitoringSystem(logger)
    
    app = GUI(alarm_manager, monitoring_system, logger)
    app.run()


if __name__ == "__main__":
    main()