# 2153689

from heapsort.visual import Visualizer
from heapsort.draw import Button, Label
from heapsort.tools import insert_newlines
from map.get_station import get_lines, update
from map.map import Map
from map.path import Path
from map.draw_map import clear_paths, draw_paths
from map.add import add_connect, add_points

import os
import tkinter as tk
from tkinter import ttk


class Metro:
    def __init__(self, dir) -> None:
        self.dir = dir
        self.lines_path = os.path.join(dir, 'data', 'lines.json')
        self.icon_path = os.path.join(dir, 'data', 'icon.ico')
        self.label_length = 20

        self.stations = []
        self.lines = []

    def init(self):
        self.visualizer = Visualizer(self.dir)

        self.Button1 = Button(self.visualizer.root)
        self.Button2 = Button(self.visualizer.root)
        self.Button3 = Button(self.visualizer.root)
        self.Button4 = Button(self.visualizer.root)
        self.Button5 = Button(self.visualizer.root)
        self.Label1 = Label(self.visualizer.root)
        self.Label2 = Label(self.visualizer.root)
        self.Label3 = Label(self.visualizer.root)

        self.svalue1 = tk.StringVar()
        self.svalue2 = tk.StringVar()
        self.svalue3 = tk.StringVar()
        self.svalue4 = tk.StringVar()

        self.Combo1 = ttk.Combobox(
            self.visualizer.root, state="readonly", font=('Helvetica', 10))
        self.Combo2 = ttk.Combobox(
            self.visualizer.root, state="readonly", font=('Helvetica', 10))
        self.Combo3 = ttk.Combobox(
            self.visualizer.root, state="readonly", font=('Helvetica', 10))
        self.Combo4 = ttk.Combobox(
            self.visualizer.root, state="readonly", font=('Helvetica', 10))

        self.map = Map(self.visualizer.root)

    def update_station_info(self):
        update(self.lines_path)
        self.visualizer.close_canvas()
        self.draw_main_window(True)

    def get_station_info(self):
        self.lines = get_lines(self.lines_path)

    def get_departure_arrival(self):
        values1, values2 = [], []
        for line in self.lines:
            values1.append(line[1])
        self.Combo1['values'] = values1
        self.Combo1.set(self.lines[0][1])
        self.Combo2['values'] = values1
        self.Combo2.set(self.lines[0][1])

        for station in self.lines[0][3]:
            values2.append(station[1])
        self.Combo3['values'] = values2
        self.Combo3.set(self.lines[0][3][0][1])
        self.Combo4['values'] = values2
        self.Combo4.set(self.lines[0][3][0][1])

    def on_select1(self, event):
        sline = self.Combo1.get()
        for line in self.lines:
            if line[1] == sline:
                values = []
                for station in line[3]:
                    values.append(station[1])
                self.Combo3['values'] = values
                if len(line[3]) > 0:
                    self.Combo3.set(line[3][0][1])
                else:
                    self.Combo3.set("")
                return

    def on_select2(self, event):
        sline = self.Combo2.get()
        for line in self.lines:
            if line[1] == sline:
                values = []
                for station in line[3]:
                    values.append(station[1])
                self.Combo4['values'] = values
                if len(line[3]) > 0:
                    self.Combo4.set(line[3][0][1])
                else:
                    self.Combo4.set("")
                return

    def on_select(self, event):
        self.map.frame.focus_get()

    def get_path(self):
        self.map.paths = clear_paths(self.map.map, self.map.paths)

        start_station = self.Combo3.get()
        end_station = self.Combo4.get()
        start, end = "", ""
        for line in self.lines:
            for station in line[3]:
                if station[1] == start_station:
                    start = station[0]
                    break
            if start != "":
                break
        for line in self.lines:
            for station in line[3]:
                if station[1] == end_station:
                    end = station[0]
                    break
            if end != "":
                break
        npath = []
        path, pathf = self.path.shortest_path(start, end)
        if path == None:
            text = "找不到路径"
        else:
            for index, station_id in enumerate(path):
                for line in self.lines:
                    found = False
                    for station in line[3]:
                        if station[0] == station_id:
                            found = True
                            if station[2] or index == 0 or index == len(path) - 1:
                                npath.append(station[1])
                            break
                    if found:
                        break
            text = ", ".join(npath)
            for index in range(1, len(pathf)):
                self.map.paths = draw_paths(
                    self.map.map, self.map.points, pathf[index], pathf[index-1], self.map.paths)
        text = insert_newlines("路线："+text, 20)
        self.Label3.display_label(text, 10, 160, 20, 10)

    def add_new_point(self):
        add_points(self.visualizer.root, self.icon_path, self.lines,
                   self.map.map, self.map.Ax, self.map.Ay, self.map.points)

    def add_new_line(self):
        add_connect(self.visualizer.root, self.icon_path, self.lines,
                    self.map.map, self.map.Ax, self.map.Ay, self.map.lsegs, self.map.points, self.path.graph)

    def transfer(self, event):
        if event.keysym == "Up":
            self.map.move_canvas("up")
        elif event.keysym == "Down":
            self.map.move_canvas("down")
        elif event.keysym == "Left":
            self.map.move_canvas("left")
        elif event.keysym == "Right":
            self.map.move_canvas("right")
        elif event.keysym == "minus":
            self.map.move_canvas("small")
        elif event.keysym == "equal":
            self.map.move_canvas("large")
        return "break"

    def draw_main_window(self, updated=False):
        self.init()
        self.get_station_info()

        self.visualizer.root.title("上海地铁换乘指南")

        self.Button1.draw(10, 10, self.label_length,
                          2, "更新数据", "lightblue", "lightcyan", self.update_station_info)

        self.Button2.draw(10, 540, self.label_length,
                          2, "关闭窗口", "red", "pink", self.visualizer.close_canvas)

        self.Button3.draw(10, 360, self.label_length,
                          2, "计算最短路径", "lightblue", "lightcyan", self.get_path)

        self.Button4.draw(10, 415, 9, 2, "添加站点", "lightblue",
                          "lightcyan", self.add_new_point)
        self.Button5.draw(108, 415, 9, 2, "添加线路",
                          "lightblue", "lightcyan", self.add_new_line)

        self.Label1.display_label("出发站", 12, 70, 9, 1)
        self.Label2.display_label("到达站", 110, 70, 9, 1)
        if updated:
            self.Label3.display_label("更新数据成功", 10, 160, 20, 10)

        self.Combo1.place(x=12, y=100, width=90, height=28)
        self.Combo2.place(x=108, y=100, width=90, height=28)
        self.Combo3.place(x=12, y=130, width=90, height=28)
        self.Combo4.place(x=108, y=130, width=90, height=28)

        self.Combo1.bind("<<ComboboxSelected>>", self.on_select1)
        self.Combo2.bind("<<ComboboxSelected>>", self.on_select2)
        self.Combo3.bind("<<ComboboxSelected>>", self.on_select)
        self.Combo4.bind("<<ComboboxSelected>>", self.on_select)

        self.Combo1.bind("<KeyPress>", self.transfer)
        self.Combo2.bind("<KeyPress>", self.transfer)
        self.Combo3.bind("<KeyPress>", self.transfer)
        self.Combo4.bind("<KeyPress>", self.transfer)

        self.get_departure_arrival()

        self.path = Path(self.lines)

        self.map.draw_map(self.lines)

        self.visualizer.run()
