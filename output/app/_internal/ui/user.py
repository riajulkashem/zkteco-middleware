import tkinter as tk
from tkinter import messagebox

from ui.components import (
    create_header,
    create_dropdown,
    create_label_entry_row,
    create_table_headers,
)
from ui.components.edit_form import DynamicEditForm
from ui.components.layout import create_icon_button
from ui.utils.theme_utils import (
    GREEN_COLOUR,
    WHITE_COLOR,
    FONT_HELVETICA,
    BIG_SCREEN_SIZE,
)


class UserManagementUI:
    def __init__(self, root, logic, navigate):
        self.root = root
        self.navigate = navigate
        self.logic = logic
        self.device_map = {}
        self.setup_ui()

    def setup_ui(self):
        self.root.title("ZkTeco Connector Made By Riajul Kashem")
        self.root.geometry(BIG_SCREEN_SIZE)
        self.root.resizable(False, False)
        self.root.configure(bg=WHITE_COLOR)

        create_header(self.root, "👥 User Management")

        self.input_frame = tk.Frame(self.root, bg=WHITE_COLOR)
        self.input_frame.pack(fill="x", padx=10, pady=5)

        self.name_entry = tk.Entry(self.input_frame, width=15)
        self.privilege_entry = tk.Entry(self.input_frame, width=10)
        self.password_entry = tk.Entry(self.input_frame, width=10, show="*")
        self.user_id_entry = tk.Entry(self.input_frame, width=10)
        self.group_id_entry = tk.Entry(self.input_frame, width=10)

        devices = self.logic.get_devices()
        self.device_map = {d["name"]: d["id"] for d in devices}
        self.device_var, self.device_dropdown = create_dropdown(
            self.input_frame, [""] + list(self.device_map.keys()), width=10
        )

        # Arrange labels and fields
        create_label_entry_row(
            self.input_frame,
            [
                ("Name:", self.name_entry),
                ("Privilege:", self.privilege_entry),
                ("Password:", self.password_entry),
                ("User ID:", self.user_id_entry),
                ("Group ID:", self.group_id_entry),
                ("Device:", self.device_dropdown),
            ],
        )

        tk.Button(
            self.input_frame,
            text="Add User",
            bg=WHITE_COLOR,
            fg=GREEN_COLOUR,
            font=(FONT_HELVETICA, 10),
            command=self.handle_add_user,
            relief="flat",
            borderwidth=0,
        ).grid(row=1, column=6, padx=10, pady=2)

        self.table_frame = tk.Frame(self.root, bg=WHITE_COLOR)
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        create_table_headers(
            self.table_frame,
            ["ID", "Name", "Privilege", "User ID", "Group ID", "Device", "Actions"],
        )

        self.back_frame = tk.Frame(self.root, bg=WHITE_COLOR)
        self.back_frame.pack(fill="x", pady=5)

        tk.Button(
            self.back_frame,
            text="Back to Dashboard",
            bg="#34C759",
            fg="black",
            font=(FONT_HELVETICA, 10),
            command=self.go_back,
            relief="flat",
            borderwidth=0,
        ).pack(side="right", padx=10)

        self.display_users()

    def display_users(self):
        for widget in self.table_frame.winfo_children():
            if widget.grid_info().get("row", 0) > 0:
                widget.destroy()

        users = self.logic.get_users()
        for row, user in enumerate(users, start=1):
            for col, value in enumerate(
                [
                    user["id"],
                    user["name"],
                    user["privilege"],
                    user["user_id"],
                    user["group_id"],
                    user["device_name"],
                ]
            ):
                tk.Label(
                    self.table_frame,
                    text=value,
                    bg=WHITE_COLOR,
                    relief="solid",
                    padx=10,
                    pady=5,
                ).grid(row=row, column=col, sticky="nsew")

            actions_frame = tk.Frame(self.table_frame, bg=WHITE_COLOR, relief="solid")
            actions_frame.grid(row=row, column=6, sticky="nsew")

            create_icon_button(
                parent=actions_frame,
                icon="✏️",
                command=lambda idx=user["id"]: self.edit_user(idx),
            )

            create_icon_button(
                parent=actions_frame,
                icon="🗑️",
                command=lambda idx=user["id"]: self.delete_user(idx),
            )

    def handle_add_user(self):
        name = self.name_entry.get()
        privilege = self.privilege_entry.get()
        password = self.password_entry.get()
        user_id = self.user_id_entry.get()
        group_id = self.group_id_entry.get()
        device_id = self.device_map.get(self.device_var.get())

        success, message = self.logic.add_user(
            name, privilege, password, user_id, group_id, device_id
        )
        if success:
            for entry in [
                self.name_entry,
                self.privilege_entry,
                self.password_entry,
                self.user_id_entry,
                self.group_id_entry,
            ]:
                entry.delete(0, tk.END)
            self.device_var.set("")
            self.display_users()
        messagebox.showinfo("Success" if success else "Error", message)

    def edit_user(self, id_user):
        self.display_users()  # Refresh user list
        user = next((u for u in self.logic.get_users() if u["id"] == id_user), None)
        if not user:
            return messagebox.showerror("Error", "User not found.")

        config = [
            {"label": "Name:", "key": "name"},
            {"label": "Privilege:", "key": "privilege"},
            {"label": "Password:", "key": "password", "secret": True},
            {"label": "User ID:", "key": "user_id"},
            {"label": "Group ID:", "key": "group_id"},
            {"label": "Device:", "key": "device_name", "type": "dropdown"},
        ]

        def save_callback(values):
            device_id = self.device_map.get(values.pop("device_name", ""))
            return self.logic.edit_user(id_user, **values, device_id=device_id)

        DynamicEditForm(
            parent=self.root,
            title="Edit User",
            config=config,
            data=user,
            save_callback=save_callback,
            draw_table_callback=self.display_users,
            dropdown_options={"device_name": [""] + list(self.device_map.keys())},
        )

    def delete_user(self, user_id):
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this user?"):
            success, message = self.logic.delete_user(user_id)
            if success:
                self.display_users()
            messagebox.showinfo("Success" if success else "Error", message)

    def go_back(self):
        if self.navigate:
            self.navigate("dashboard")
