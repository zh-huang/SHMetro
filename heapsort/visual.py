# 2153689

import tkinter as tk
import time
import os

radius = 15


class Visualizer:
    def __init__(self, dir, width=800, height=600):
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=width, height=height)
        self.root.protocol("WM_DELETE_WINDOW", self.close_canvas)
        self.canvas.pack()
        icon_path = os.path.join(dir, 'data', 'icon.ico')
        self.root.iconbitmap(icon_path)
        
        self.nodes = []
        self.lines = []
        self.afters = []

    def close_canvas(self):
        self.clear()
        self.root.destroy()

    def draw_circle(self, x, y, text):
        circle = self.canvas.create_oval(
            x - radius, y - radius, x + radius, y + radius, fill="cyan")
        text = self.canvas.create_text(x, y, text=str(text))
        self.nodes.append((circle, text))

    def connect_circles(self, index1, index2):
        x1, y1, _, _ = self.canvas.coords(self.nodes[index1][0])
        x2, y2, _, _ = self.canvas.coords(self.nodes[index2][0])
        line = [self.canvas.create_line(
            x1 + radius, y1 + radius, x2 + radius, y2 + radius), index1, index2]
        self.canvas.tag_lower(line[0])
        self.lines.append(line)

    def change_color(self, index, color):
        self.canvas.itemconfig(self.nodes[index][0], fill=color)

    def swap_circles(self, index1, index2):
        x1, y1, _, _ = self.canvas.coords(self.nodes[index1][0])
        x2, y2, _, _ = self.canvas.coords(self.nodes[index2][0])

        for _ in range(2):
            self.canvas.itemconfig(self.nodes[index1][0], fill="red")
            self.canvas.itemconfig(self.nodes[index2][0], fill="red")
            self.root.update()
            time.sleep(.1)
            self.canvas.itemconfig(self.nodes[index1][0], fill="cyan")
            self.canvas.itemconfig(self.nodes[index2][0], fill="cyan")
            self.root.update()
            time.sleep(.1)

        for line in self.lines:
            if line[1] == index1 and line[2] == index2 or line[1] == index2 and line[2] == index1:
                self.canvas.itemconfig(line[0], state="hidden")
                break

        for line in self.lines:
            for i in range(1, len(line)):
                if line[i] == index1 or line[i] == index2:
                    line[i] = index1 + index2 - line[i]

        x1_step = (x2 - x1) / 10
        y1_step = (y2 - y1) / 10
        x2_step = (x1 - x2) / 10
        y2_step = (y1 - y2) / 10

        for _ in range(10):
            x1 += x1_step
            y1 += y1_step
            x2 += x2_step
            y2 += y2_step
            self.canvas.move(self.nodes[index1][0], x1_step, y1_step)
            self.canvas.move(self.nodes[index1][1], x1_step, y1_step)
            self.canvas.move(self.nodes[index2][0], x2_step, y2_step)
            self.canvas.move(self.nodes[index2][1], x2_step, y2_step)
            self.root.update()
            tmp_id = self.root.after(50)
            self.afters.append(tmp_id)

        for line in self.lines:
            if line[1] == index1 and line[2] == index2 or line[1] == index2 and line[2] == index1:
                self.canvas.itemconfig(line[0], state="normal")
                self.canvas.tag_lower(line[0])

    def clear(self):
        root = self.root
        for id in self.afters:
            try:
                root.after_cancel(id)
            except:
                pass
        self.afters = []

        for node in self.nodes:
            self.canvas.delete(node[0])
            self.canvas.delete(node[1])
        self.nodes = []

        for line in self.lines:
            self.canvas.delete(line[0])
        self.lines = []

    def run(self):
        self.root.mainloop()
