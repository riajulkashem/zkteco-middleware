import tkinter as tk
from tkinter import messagebox

from database_manager import DatabaseManager
from ui.utils.theme_utils import (
    GREEN_COLOUR,
    WHITE_COLOR,
    FONT_HELVETICA,
    DEFAULT_SCREEN_SIZE,
)


class SettingsWindow:
    def __init__(self, root, navigate):
        self.root = root
        self.navigate = navigate
        self.db_manager = DatabaseManager()
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Database Setup")
        self.root.geometry(DEFAULT_SCREEN_SIZE)
        self.root.resizable(False, False)
        self.root.configure(bg=GREEN_COLOUR)

        # Center Setup Button
        self.setup_button = tk.Button(
            self.root,
            text="Setup Database",
            bg=WHITE_COLOR,
            fg=GREEN_COLOUR,
            font=(FONT_HELVETICA, 14, "bold"),
            command=self.handle_setup,
            relief="flat",
            borderwidth=0,
            width=20,
            height=2,
        )
        self.setup_button.place(relx=0.5, rely=0.5, anchor="center")

    def handle_setup(self):
        success, message = self.db_manager.initialize_tables()
        messagebox.showinfo("Success" if success else "Error", message)
        if success:
            self.go_to_dashboard()

    def go_to_dashboard(self):
        if self.navigate:
            self.navigate("dashboard")
