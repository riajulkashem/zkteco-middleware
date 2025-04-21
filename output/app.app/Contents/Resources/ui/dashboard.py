import threading
import tkinter as tk
from tkinter import messagebox

from ui.components import create_header, create_button, create_card
from ui.utils.theme_utils import (
    GREEN_COLOUR,
    WHITE_COLOR,
    FONT_HELVETICA,
    DEFAULT_SCREEN_SIZE,
)


class DashboardUI:
    def __init__(self, root, logic, navigate):
        self.root = root
        self.navigate = navigate
        self.logic = logic
        self.is_syncing = False
        self.animation_chars = ["|", "/", "-", "\\"]
        self.animation_index = 0
        self.setup_ui()

    def setup_ui(self):
        self.root.title("ZkTeco Connector Made By Riajul Kashem")
        self.root.geometry(DEFAULT_SCREEN_SIZE)
        self.root.resizable(False, False)
        self.root.configure(bg=WHITE_COLOR)

        create_header(self.root, "DASHBOARD")

        self.stats_frame = tk.Frame(self.root, bg=WHITE_COLOR)
        self.stats_frame.pack(pady=10, fill="both", expand=True)

        for i in range(2):
            self.stats_frame.grid_columnconfigure(i, weight=1)
            self.stats_frame.grid_rowconfigure(i, weight=1)

        self.update_cards()

        # Buttons
        self.button_frame = tk.Frame(self.root, bg=GREEN_COLOUR)
        self.button_frame.pack(pady=10)

        create_button(self.button_frame, "SYNC NOW", self.handle_sync).pack(
            side="left", padx=5
        )
        create_button(
            self.button_frame, "DEVICES", lambda: self.navigate("devices")
        ).pack(side="left", padx=5)
        create_button(self.button_frame, "USERS", lambda: self.navigate("users")).pack(
            side="left", padx=5
        )
        create_button(self.button_frame, "Quit", lambda: self.root.destroy()).pack(
            side="left", padx=5
        )

        self.sync_status_label = tk.Label(
            self.root,
            text="Last Synced: Never",
            font=(FONT_HELVETICA, 9),
            bg=GREEN_COLOUR,
            fg="black",
        )
        self.sync_status_label.pack(pady=5)

    def update_cards(self):
        for widget in self.stats_frame.winfo_children():
            widget.destroy()

        for card in self.logic.get_card_data():
            create_card(
                parent=self.stats_frame,
                label=card["label"],
                value=card["value"],
                icon=card["icon"],
                row=card["row"],
                col=card["col"],
                font_size=card["font_size"],
            )

    def animate_sync(self):
        """Update sync status label with rotating animation."""
        if not self.is_syncing:
            return
        char = self.animation_chars[self.animation_index]
        self.sync_status_label.config(text=f"Syncing... {char}")
        self.animation_index = (self.animation_index + 1) % len(self.animation_chars)
        self.root.after(200, self.animate_sync)

    def handle_sync(self):
        """Handle sync button click with animation and async data sync."""
        if self.is_syncing:
            return

        self.is_syncing = True
        self.animate_sync()

        def sync_and_update():
            try:
                sync_time = self.logic.sync_data()
                self.root.after(0, lambda: self.post_sync(sync_time))
            except Exception:
                self.root.after(
                    0,
                    lambda: messagebox.showerror(
                        "Sync Error", f"Failed to sync: {str(e)}"
                    ),
                )
                self.root.after(0, lambda: self.post_sync(None))

        threading.Thread(target=sync_and_update, daemon=True).start()

    def post_sync(self, sync_time):
        """Update UI after sync completes."""
        self.is_syncing = False
        if sync_time:
            self.sync_status_label.config(text=f"Last Synced: {sync_time}")
            messagebox.showinfo(
                "Sync",
                "Data synced successfully! Go to the User Management screen to view updated users.",
            )
            self.update_cards()
        else:
            self.sync_status_label.config(
                text="Last Synced: Failed", bg="red", fg="white"
            )
