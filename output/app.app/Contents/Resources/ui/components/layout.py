import tkinter as tk
from tkinter import ttk

from ui.utils.theme_utils import WHITE_COLOR, FONT_HELVETICA, GREEN_COLOUR


def create_label_entry_row(parent, fields):
    for i, (label_text, widget) in enumerate(fields):
        tk.Label(
            parent, text=label_text, bg=WHITE_COLOR, font=(FONT_HELVETICA, 10)
        ).grid(row=0, column=i, padx=5, pady=2)
        widget.grid(row=1, column=i, padx=5, pady=2)


def create_dropdown(parent, options, width=15):
    var = tk.StringVar(parent)
    dropdown = ttk.OptionMenu(parent, var, options[0], *options)
    dropdown.config(width=width)
    return var, dropdown


def create_header(parent, title):
    header_frame = tk.Frame(parent, bg=GREEN_COLOUR)
    header_frame.pack(fill="x")
    tk.Label(
        header_frame,
        text=title,
        font=(FONT_HELVETICA, 14, "bold"),
        bg=GREEN_COLOUR,
        fg=WHITE_COLOR,
    ).pack(fill="x", padx=10, pady=5)


def create_table_headers(parent, headers):
    for col, header in enumerate(headers):
        tk.Label(
            parent,
            text=header,
            font=(FONT_HELVETICA, 10, "bold"),
            bg=GREEN_COLOUR,
            fg=WHITE_COLOR,
            relief="solid",
            padx=10,
            pady=5,
        ).grid(row=0, column=col, sticky="nsew")
        parent.grid_columnconfigure(col, weight=1)


def create_card(parent, label, value, icon, row, col, font_size):
    frame = tk.Frame(parent, bg=WHITE_COLOR, bd=1, relief="solid", padx=15, pady=10)
    frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
    tk.Label(frame, text=icon, font=(FONT_HELVETICA, 16), bg=WHITE_COLOR).pack(
        expand=True
    )
    tk.Label(frame, text=label, font=(FONT_HELVETICA, 10), bg=WHITE_COLOR).pack(
        expand=True
    )
    tk.Label(
        frame, text=value, font=(FONT_HELVETICA, font_size, "bold"), bg=WHITE_COLOR
    ).pack(expand=True)


def create_button(parent, text, command):
    return tk.Button(
        parent,
        text=text,
        bg=WHITE_COLOR,
        fg=GREEN_COLOUR,
        font=(FONT_HELVETICA, 10, "bold"),
        command=command,
        relief="flat",
        borderwidth=0,
    )


def create_icon_button(
    parent, icon, command, side="left", padding=2, bg=WHITE_COLOR, fg="black"
):
    button = tk.Button(parent, text=icon, bg=bg, fg=fg, bd=0, command=command)
    button.pack(side=side, padx=padding)
    return button


def create_labeled_dropdown(
    parent,
    label_text,
    variable,
    options,
    row,
    column,
    width=10,
    font=None,
    bg="#FFFFFF",
):
    tk.Label(parent, text=label_text, bg=bg, font=font).grid(
        row=row, column=column, padx=5, pady=2, sticky="w"
    )
    dropdown = ttk.OptionMenu(parent, variable, options[0], *options)
    dropdown.config(width=width)
    dropdown.grid(row=row + 1, column=column, padx=5, pady=2)
    return dropdown


def create_labeled_entry(
    parent, label_text, row, column, width=20, show=None, font=None, bg="#FFFFFF"
):
    label = tk.Label(parent, text=label_text, bg=bg, font=font)
    label.grid(row=row, column=column, padx=5, pady=2, sticky="w")
    entry = tk.Entry(parent, width=width, show=show)
    entry.grid(row=row + 1, column=column, padx=5, pady=2)

    return entry
