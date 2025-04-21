import tkinter as tk
from tkinter import messagebox

from ui.components import (
    create_header,
    create_label_entry_row,
    create_table_headers,
    create_button,
)
from ui.components.edit_form import DynamicEditForm
from ui.components.layout import create_icon_button
from ui.utils.theme_utils import WHITE_COLOR, BIG_SCREEN_SIZE


class DeviceManagementUI:
    def __init__(self, root, logic, navigate):
        self.root = root
        self.navigate = navigate
        self.logic = logic
        self.form_fields = {}  # Field name -> Entry widget
        self.columns = ["name", "ip", "port", "device_model", "serial_number"]
        self.setup_ui()

    def setup_ui(self):
        self.root.title("ZkTeco Connector Made By Riajul Kashem")
        self.root.geometry(BIG_SCREEN_SIZE)
        self.root.resizable(False, False)
        self.root.configure(bg=WHITE_COLOR)

        # Header
        create_header(self.root, "🖥️ Device Management")

        # Input form section
        self.input_frame = tk.Frame(self.root, bg=WHITE_COLOR)
        self.input_frame.pack(fill="x", padx=10, pady=5)

        entries = []
        for col_name in self.columns:
            entry = tk.Entry(self.input_frame, width=15)
            self.form_fields[col_name] = entry
            entries.append((col_name.replace("_", " ").title() + ":", entry))

        create_label_entry_row(self.input_frame, entries)

        create_button(
            self.input_frame, text="Add Device", command=self.handle_add_device
        ).grid(row=1, column=len(entries), padx=10, pady=2)

        # Table section
        self.table_frame = tk.Frame(self.root, bg=WHITE_COLOR)
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        create_table_headers(
            self.table_frame,
            ["ID"]
            + [col.replace("_", " ").title() for col in self.columns]
            + ["Actions"],
        )

        # Navigation section
        self.back_frame = tk.Frame(self.root, bg=WHITE_COLOR)
        self.back_frame.pack(fill="x", pady=5)

        create_button(
            self.back_frame, text="Back to Dashboard", command=self.go_back
        ).pack(side="right", padx=10)

        self.display_devices()

    def display_devices(self):
        for widget in self.table_frame.winfo_children():
            if widget.grid_info().get("row", 0) > 0:
                widget.destroy()

        devices = self.logic.get_devices()
        for row, device in enumerate(devices, start=1):
            # Static ID column
            tk.Label(
                self.table_frame,
                text=device["id"],
                bg=WHITE_COLOR,
                relief="solid",
                padx=10,
                pady=5,
            ).grid(row=row, column=0, sticky="nsew")

            # Dynamic fields
            for col_index, col_name in enumerate(self.columns, start=1):
                tk.Label(
                    self.table_frame,
                    text=device.get(col_name, ""),
                    bg=WHITE_COLOR,
                    relief="solid",
                    padx=10,
                    pady=5,
                ).grid(row=row, column=col_index, sticky="nsew")

            # Action buttons
            actions_frame = tk.Frame(self.table_frame, bg=WHITE_COLOR, relief="solid")
            actions_frame.grid(row=row, column=len(self.columns) + 1, sticky="nsew")

            create_icon_button(
                parent=actions_frame,
                icon="✏️",
                command=lambda idx=device["id"]: self.edit_device(idx),
            )

            create_icon_button(
                parent=actions_frame,
                icon="🗑️",
                command=lambda idx=device["id"]: self.delete_device(idx),
            )

    def handle_add_device(self):
        values = {field: entry.get() for field, entry in self.form_fields.items()}
        success, message = self.logic.add_device(**values)

        if success:
            for entry in self.form_fields.values():
                entry.delete(0, tk.END)
            self.display_devices()

        messagebox.showinfo("Success" if success else "Error", message)

    def edit_device(self, device_id):
        self.display_devices()  # Refresh device list
        device = next(
            (d for d in self.logic.get_devices() if d["id"] == device_id), None
        )
        if not device:
            return messagebox.showerror("Error", "Device not found.")

        config = [
            {"label": "Name:", "key": "name"},
            {"label": "Device Model:", "key": "device_model"},
            {"label": "Serial Number:", "key": "serial_number"},
            {"label": "IP:", "key": "ip"},
            {"label": "Port:", "key": "port"},
        ]

        def save_callback(values):
            # Validate required fields
            required_fields = ["name", "device_model", "serial_number", "ip", "port"]
            for field in required_fields:
                if not values.get(field):
                    return False, f"{field.replace('_', ' ').title()} is required."

            try:
                values["port"] = int(values["port"])
            except ValueError:
                return False, "Port must be a number."

            success, message = self.logic.edit_device(device_id, **values)
            if success:
                self.display_devices()
            return success, message

        DynamicEditForm(
            parent=self.root,
            title="Edit Device",
            config=config,
            data=device,
            save_callback=save_callback,
            draw_table_callback=self.display_devices,
            dropdown_options={},
        )

    def delete_device(self, device_id):
        if messagebox.askyesno(
            "Confirm", "Are you sure you want to delete this device?"
        ):
            success, message = self.logic.delete_device(device_id)
            if success:
                self.display_devices()
            messagebox.showinfo("Success" if success else "Error", message)

    def go_back(self):
        if self.navigate:
            self.navigate("dashboard")
