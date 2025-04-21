import tkinter as tk
from tkinter import ttk, messagebox


from database_manager import DatabaseManager
from ui.utils.theme_utils import (
    BLUE_COLOUR,
    WHITE_COLOR,
    FONT_HELVETICA,
    DEFAULT_SCREEN_SIZE,
)


class LoginWindow:
    def __init__(self, root, navigate):
        self.root = root
        self.navigate = navigate
        self.setup_ui()

    def setup_ui(self):
        self.root.title("ZkTeco Connector Made By Riajul Kashem")
        self.root.geometry(DEFAULT_SCREEN_SIZE)
        self.root.resizable(False, False)

        # Left Panel (Blue)
        self.left_frame = tk.Frame(self.root, bg=BLUE_COLOUR, width=250)
        self.left_frame.pack(side="left", fill="both")

        tk.Label(
            self.left_frame,
            text="Welcome to Middleware App",
            fg=WHITE_COLOR,
            bg=BLUE_COLOUR,
            font=(FONT_HELVETICA, 16, "bold"),
            wraplength=200,
            justify="left",
        ).place(x=20, y=100)

        tk.Label(
            self.left_frame,
            text="Securely connect and monitor ZKTeco devices.",
            fg=WHITE_COLOR,
            bg=BLUE_COLOUR,
            font=(FONT_HELVETICA, 10),
            wraplength=200,
            justify="left",
        ).place(x=20, y=160)

        # Right Panel (White)
        self.right_frame = tk.Frame(self.root, bg=WHITE_COLOR)
        self.right_frame.pack(side="right", expand=True, fill="both")

        tk.Label(
            self.right_frame,
            text="User Login",
            font=(FONT_HELVETICA, 14, "bold"),
            bg=WHITE_COLOR,
            fg=BLUE_COLOUR,
        ).place(x=60, y=80)

        # Email
        tk.Label(
            self.right_frame,
            text="Email:",
            bg=WHITE_COLOR,
            font=(FONT_HELVETICA, 10),
        ).place(x=60, y=140)
        self.email_entry = ttk.Entry(self.right_frame, width=25)
        self.email_entry.place(x=60, y=165)

        # Password
        tk.Label(
            self.right_frame,
            text="Password:",
            bg=WHITE_COLOR,
            font=(FONT_HELVETICA, 10),
        ).place(x=60, y=200)
        self.password_entry = ttk.Entry(self.right_frame, show="*", width=25)
        self.password_entry.place(x=60, y=225)

        # Login Button
        self.login_button = tk.Button(
            self.right_frame,
            text="Login",
            command=self.handle_login,
            bg=BLUE_COLOUR,
            fg=WHITE_COLOR,
            font=(FONT_HELVETICA, 11, "bold"),
            relief="flat",
            width=15,
            pady=5,
        )
        self.login_button.place(relx=0.5, y=280, anchor="center")

    def check_database(self):
        # Try connecting and checking for expected table
        try:
            db = DatabaseManager()
            # We'll check if the 'users' table has at least one user
            users = db.get_users()
            print("users: ", users)
            self.go_to_dashboard()
        except Exception as e:
            # Unexpected error, still redirect
            print("Unexpected DB issue:", str(e))
            self.redirect_to_settings()

    def handle_login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if email == "admin" and password == "admin":
            self.check_database()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")

    def redirect_to_settings(self):
        if self.navigate:
            self.navigate("settings")

    def go_to_dashboard(self):
        if self.navigate:
            self.navigate("dashboard")
