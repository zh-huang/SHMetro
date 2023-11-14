import tkinter as tk
from heapsort.draw import Button, Label, Input
from map.affine import Affine
from map.draw_map import draw_lines, zoom_in, zoom_out

import copy

LEFT = 200
UP = 0
WIDTH = 800
HEIGHT = 600
RADIUS = 5
SCALE = 0.1


class Map:
    def __init__(self, root) -> None:
        self.root = root
        self.points = []
        self.lsegs = []
        self.paths = []

    def draw_main_window(self):
        root = self.root

        self.frame = tk.Frame(root, width=WIDTH-LEFT-4, height=HEIGHT-UP-4,
                              highlightbackground="pink", highlightcolor="pink", highlightthickness=2)
        frame = self.frame
        frame.place(x=LEFT, y=UP)

        self.map = tk.Canvas(frame, width=WIDTH-LEFT-4, height=HEIGHT-UP-4)
        map = self.map
        map.pack(fill=tk.BOTH, expand=True)
    
    def get_scale(self):
        left, right, up, down = float(360), float(0), float(180), float(0)
        LEFT, RIGHT, UP, DOWN = float(0), float(600), float(0), float(600)
        
        for line in self._lines:
            _, _, _, stations = line
            for station in stations:
                if float(station[3]) < left:
                    left = float(station[3])
                if float(station[3]) > right:
                    right = float(station[3])
                if float(station[4]) < up:
                    up = float(station[4])
                if float(station[4]) > down:
                    down = float(station[4])
                
        self.Ax = Affine(left, right, LEFT, RIGHT)
        self.Ay = Affine(up, down, UP, DOWN)
        return self.Ax, self.Ay

    def zoom(self, event):
        x = self.map.canvasx(event.x)
        y = self.map.canvasy(event.y)
        delta = event.delta
        if delta > 0:
            zoom_in(self.map, self.points, self.lsegs, self.paths, x, y)
        elif delta < 0:
            zoom_out(self.map, self.points, self.lsegs, self.paths, x, y)

    def move_canvas(self, direction):
        x = self.map.winfo_width() // 2
        y = self.map.winfo_height() // 2
        if direction == "up":
            self.map.yview_scroll(-1, "units")
        elif direction == "down":
            self.map.yview_scroll(1, "units")
        elif direction == "left":
            self.map.xview_scroll(-1, "units")
        elif direction == "right":
            self.map.xview_scroll(1, "units")
        elif direction == "large":
            zoom_in(self.map, self.points, self.lsegs, self.paths, x, y)
        elif direction == "small":
            zoom_out(self.map, self.points, self.lsegs, self.paths, x, y)

    def move(self):
        root = self.root

        self.Button_UP = Button(root)
        self.Button_DOWN = Button(root)
        self.Button_LEFT = Button(root)
        self.Button_RIGHT = Button(root)
        self.Button_LARGE = Button(root)
        self.Button_SMALL = Button(root)

        self.Button_SMALL.draw(10, 470, 6, 1, "-", "gray", "white")
        self.Button_UP.draw(73, 470, 6, 1, "上", "pink", "purple")
        self.Button_LARGE.draw(136, 470, 6, 1, "+", "gray", "white")
        self.Button_LEFT.draw(10, 505, 6, 1, "左", "pink", "purple")
        self.Button_DOWN.draw(73, 505, 6, 1, "下", "pink", "purple")
        self.Button_RIGHT.draw(136, 505, 6, 1, "右", "pink", "purple")

        self.Button_UP.button.configure(command=lambda: self.move_canvas("up"))
        self.Button_DOWN.button.configure(
            command=lambda: self.move_canvas("down"))
        self.Button_LEFT.button.configure(
            command=lambda: self.move_canvas("left"))
        self.Button_RIGHT.button.configure(
            command=lambda: self.move_canvas("right"))
        self.Button_LARGE.button.configure(
            command=lambda: self.move_canvas("large"))
        self.Button_SMALL.button.configure(
            command=lambda: self.move_canvas("small"))

    def key_bound(self):
        root = self.root
        root.bind("<Up>", lambda event: self.move_canvas("up"))
        root.bind("<Down>", lambda event: self.move_canvas("down"))
        root.bind("<Left>", lambda event: self.move_canvas("left"))
        root.bind("<Right>", lambda event: self.move_canvas("right"))
        root.bind("<KeyPress-minus>", lambda event: self.move_canvas("small"))
        root.bind("<KeyPress-equal>", lambda event: self.move_canvas("large"))

    def draw_map(self, lines: list):
        self.draw_main_window()
        self._lines = lines
        Ax, Ay = self.get_scale()
        self.points, self.lsegs = draw_lines(self.map, lines, Ax, Ay)
        self.map.bind("<MouseWheel>", self.zoom)
        self.key_bound()
        self.move()
