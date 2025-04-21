import tkinter as tk
from database_manager import DatabaseManager
from logic.dashboard import DashboardLogic
from logic.device import DeviceManagementLogic
from logic.user import UserManagementLogic
from ui.app_settings import SettingsWindow
from ui.dashboard import DashboardUI
from ui.device import DeviceManagementUI
from ui.login import LoginWindow
from ui.user import UserManagementUI


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.db_manager = DatabaseManager()
        self.dashboard_logic = DashboardLogic(self.db_manager)
        self.device_logic = DeviceManagementLogic(self.db_manager)
        self.user_logic = UserManagementLogic(self.db_manager)
        self.screens = {
            "login": lambda root, navigate: LoginWindow(root, navigate),
            "dashboard": lambda root, navigate: DashboardUI(
                root, self.dashboard_logic, navigate
            ),
            "devices": lambda root, navigate: DeviceManagementUI(
                root, self.device_logic, navigate
            ),
            "users": lambda root, navigate: UserManagementUI(
                root, self.user_logic, navigate
            ),
            "settings": lambda root, navigate: SettingsWindow(root, navigate),
        }
        self.current_screen = None
        # TODO: implement login
        self.show_screen("login")

    def show_screen(self, screen_name):
        """Show the specified screen, hiding the current one."""
        if screen_name not in self.screens:
            raise ValueError(f"Unknown screen: {screen_name}")

        # Hide current screen
        if self.current_screen:
            if hasattr(self.current_screen, "frame"):
                self.current_screen.frame.pack_forget()
            else:
                for widget in self.root.winfo_children():
                    widget.destroy()

        # Create new screen
        self.current_screen = self.screens[screen_name](self.root, self.show_screen)

        # Pack the screen's frame (if it has one) or rely on screen to set up widgets
        if hasattr(self.current_screen, "frame"):
            self.current_screen.frame.pack(fill="both", expand=True)

    def run(self):
        """Start the Tkinter event loop."""
        self.root.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()
