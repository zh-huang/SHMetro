# 2153689

import tkinter as tk


class Label:
    def __init__(self, root) -> None:
        self.root = root
        self.label = tk.Label(root)

    def display_label(self, text, x=0, y=0, width=55, height=4):
        label = self.label
        label.config(text=text)
        label.place(x=x, y=y)
        label.configure(
            font=("Consolas", 12),
            bg="white",
            width=width,
            height=height,
            justify="left"
        )


class Input:
    def __init__(self, root) -> None:
        self.root = root
        self.text = tk.Text(root)

    def draw_input(self, x=0, y=0, width=55, height=4):
        text = self.text

        text.place(x=x, y=y)
        text.configure(
            font=("Consolas", 12),
            width=width,
            height=height
        )

class Button:
    def __init__(self, root) -> None:
        self.root = root
        self.button = tk.Button(root)
        
    def draw(self, x=0, y=0, width=55, height=4, text="", color="black", accolor="white", fun=None, L=False):
        button = self.button
        button.config(text=text)
        if fun:
            button.configure(command=fun)
        button.place(x=x, y=y)
        button.configure(
            font=("Consolas", 12),
            bg=color,
            width=width,
            height=height,
            relief="ridge",
            borderwidth=2,
            activebackground=accolor
        )
