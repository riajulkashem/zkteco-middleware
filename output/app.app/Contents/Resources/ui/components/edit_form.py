from tkinter import messagebox
import tkinter as tk

from ui.components import create_labeled_entry, create_button, create_labeled_dropdown
from ui.utils.theme_utils import WHITE_COLOR, GREEN_COLOUR


class DynamicEditForm:
    def __init__(
        self,
        parent,
        title,
        config,
        data,
        save_callback,
        draw_table_callback,
        dropdown_options=None,
    ):
        """
        Initialize a dynamic edit form.

        Args:
            parent: Parent Tkinter window/widget
            title: Form window title
            config: List of field configurations (dict with 'label', 'key', 'type', 'options' for dropdowns)
            data: Dictionary containing current data to edit
            save_callback: Function to call when saving (takes dict of updated values)
            dropdown_options: Dict of {key: options_list} for dropdown fields
        """
        self.window = tk.Toplevel(parent)
        self.window.title("ZkTeco Connector Made By Riajul Kashem")
        self.window.geometry("300x500")
        self.save_callback = save_callback
        self.draw_table_callback = draw_table_callback
        self.dropdown_options = dropdown_options or {}

        # Create main frame
        self.frame = tk.Frame(self.window, bg=WHITE_COLOR)
        self.frame.grid(padx=10, pady=5, sticky="nsew")
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

        # Add header
        header_frame = tk.Frame(self.frame, bg=GREEN_COLOUR)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        tk.Label(
            header_frame,
            text=title,
            font=("Helvetica", 14, "bold"),
            bg=GREEN_COLOUR,
            fg=WHITE_COLOR,
        ).pack(fill="x", padx=10, pady=5)

        # Create form fields
        self.entries = {}
        self.create_form_fields(config, data)

        # Add save button
        button = create_button(self.frame, text="Save", command=self.save)
        button.grid(row=len(config) * 2 + 1, column=0, pady=15)

    def create_form_fields(self, config, data):
        """Create form fields based on configuration."""
        for i, field in enumerate(config):
            key = field["key"]
            label = field["label"]
            field_type = field.get("type", "entry")

            if field_type == "dropdown":
                options = self.dropdown_options.get(key, field.get("options", [""]))
                var = tk.StringVar(value=str(data.get(key, "")))
                create_labeled_dropdown(
                    self.frame,
                    label_text=label,
                    variable=var,
                    options=options,
                    row=i * 2 + 1,  # Offset by 1 to account for header
                    column=0,
                    width=20,
                    bg=WHITE_COLOR,
                )
                self.entries[key] = var
            else:
                entry = create_labeled_entry(
                    self.frame,
                    label_text=label,
                    row=i * 2 + 1,  # Offset by 1 to account for header
                    column=0,
                    width=30,
                    show="*" if field.get("secret") else None,
                    bg=WHITE_COLOR,
                )
                entry.insert(0, str(data.get(key, "")))
                self.entries[key] = entry

    def save(self):
        """Collect form data and call save callback."""
        updated_values = {}
        for key, widget in self.entries.items():
            value = (
                widget.get()
                if isinstance(widget, (tk.Entry, tk.StringVar))
                else widget.get()
            )
            updated_values[key] = value
        success, message = self.save_callback(updated_values)
        if success:
            self.window.destroy()
            self.draw_table_callback()
        messagebox.showinfo("Success" if success else "Error", message)
