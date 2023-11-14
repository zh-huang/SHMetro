# 2153689

from map.affine import Affine

import tkinter as tk
from tkinter import ttk

RADIUS = 4


def add_points(root: tk.Tk, dir, lines, canvas: tk.Canvas, Ax: Affine, Ay: Affine, points):
    popup = tk.Toplevel(root, width=360, height=220)
    popup.title("添加站点")
    popup.iconbitmap(dir)

    label1 = tk.Label(popup, text="站点ID")
    label1.place(x=10, y=10)
    label1.configure(font=("Consolas", 12), width=8, justify="left")
    entry1 = tk.Entry(popup)
    entry1.place(x=110, y=10)
    entry1.configure(font=("Consolas", 12), width=24, justify="left")

    label2 = tk.Label(popup, text="站点名称")
    label2.place(x=10, y=50)
    label2.configure(font=("Consolas", 12), width=8, justify="left")
    entry2 = tk.Entry(popup)
    entry2.place(x=110, y=50)
    entry2.configure(font=("Consolas", 12), width=24, justify="left")

    label3 = tk.Label(popup, text="经度")
    label3.place(x=10, y=90)
    label3.configure(font=("Consolas", 12), width=8, justify="left")
    entry3 = tk.Entry(popup)
    entry3.place(x=110, y=90)
    entry3.configure(font=("Consolas", 12), width=24, justify="left")

    label4 = tk.Label(popup, text="纬度")
    label4.place(x=10, y=130)
    label4.configure(font=("Consolas", 12), width=8, justify="left")
    entry4 = tk.Entry(popup)
    entry4.place(x=110, y=130)
    entry4.configure(font=("Consolas", 12), width=24, justify="left")

    label5 = tk.Label(popup, text="")
    label5.place(x=10, y=160)

    def submit():
        nonlocal lines, canvas, Ax, Ay, points

        if not entry1.get() or not entry2.get() or not entry3.get() or not entry4.get():
            label5.configure(fg="red", text="错误：需要填写所有字段")
            return None

        try:
            lat = float(entry3.get())
            lon = float(entry4.get())
        except:
            label5.configure(fg="red", text="错误：经度和纬度必须为数字")
            return None

        point = [entry1.get(), entry2.get(), False, lat, lon]
        lines[-1][3].append(point)

        x, y = Ax.Forward(lat), Ay.Forward(lon)
        nid = canvas.create_oval(x - RADIUS, y - RADIUS, x + RADIUS,
                                 y + RADIUS, fill="white", outline="gray", width=2)
        points.append([nid, x, y, str(point[0]), str(point[1])])

        popup.destroy()

    def close():
        popup.destroy()

    button1 = tk.Button(popup, text="确认", command=submit)
    button1.place(x=170, y=180)
    button1.configure(font=("Consolas", 12), width=15, height=1,
                      relief="ridge", bg="lightblue", activebackground="lightcyan")
    button2 = tk.Button(popup, text="取消", command=close)
    button2.place(x=10, y=180)
    button2.configure(font=("Consolas", 12), width=15,
                      height=1, relief="ridge")


def add_connect(root: tk.Tk, dir, lines, canvas: tk.Canvas, Ax: Affine, Ay: Affine, lsegs, points, graph: dict):
    popup = tk.Toplevel(root, width=360, height=180)
    popup.title("添加线路连接")
    popup.iconbitmap(dir)

    label1 = tk.Label(popup, text="站点1")
    label1.place(x=10, y=10)
    label1.configure(font=("Consolas", 12), width=16)
    label2 = tk.Label(popup, text="站点2")
    label2.place(x=170, y=10)
    label2.configure(font=("Consolas", 12), width=16)

    Combo1 = ttk.Combobox(popup, state="readonly", font=('Helvetica', 12))
    Combo2 = ttk.Combobox(popup, state="readonly", font=('Helvetica', 12))
    Combo3 = ttk.Combobox(popup, state="readonly", font=('Helvetica', 12))
    Combo4 = ttk.Combobox(popup, state="readonly", font=('Helvetica', 12))

    Combo1.place(x=10, y=50, width=150, height=28)
    Combo2.place(x=170, y=50, width=150, height=28)
    Combo3.place(x=10, y=90, width=150, height=28)
    Combo4.place(x=170, y=90, width=150, height=28)

    values1, values2 = [], []
    for line in lines:
        values1.append(line[1])
    Combo1['values'] = values1
    Combo1.set(lines[0][1])
    Combo2['values'] = values1
    Combo2.set(lines[0][1])

    for station in lines[0][3]:
        values2.append(station[1])
    Combo3['values'] = values2
    Combo3.set(lines[0][3][0][1])
    Combo4['values'] = values2
    Combo4.set(lines[0][3][0][1])

    def on_select1(event):
        nonlocal Combo1, lines
        sline = Combo1.get()
        for line in lines:
            if line[1] == sline:
                values = []
                for station in line[3]:
                    values.append(station[1])
                Combo3['values'] = values
                if len(line[3]) > 0:
                    Combo3.set(line[3][0][1])
                else:
                    Combo3.set("")
                return

    def on_select2(event):
        sline = Combo2.get()
        for line in lines:
            if line[1] == sline:
                values = []
                for station in line[3]:
                    values.append(station[1])
                Combo4['values'] = values
                if len(line[3]) > 0:
                    Combo4.set(line[3][0][1])
                else:
                    Combo4.set("")
                return

    def submit():
        nonlocal lines, canvas, Ax, Ay, lsegs, points, graph

        if not Combo3.get() or not Combo4.get():
            label5.configure(fg="red", text="错误：需要选择两个站点")
            return

        start_station = Combo3.get()
        end_station = Combo4.get()

        for point in points:
            if point[4] == start_station:
                x1, y1 = point[1], point[2]
                break
        for point in points:
            if point[4] == end_station:
                x2, y2 = point[1], point[2]
                break

        line = canvas.create_line(x1, y1, x2, y2, fill="black")
        canvas.tag_lower(line)
        lsegs.append([line, x1, y1, x2, y2])
        
        id1, id2 = "", ""
        for line in lines:
            for station in line[3]:
                if station[1] == start_station:
                    id1 = station[0]
                    break
            if id1 != "":
                break
        for line in lines:
            for station in line[3]:
                if station[1] == end_station:
                    id2 = station[0]
                    break
            if id2 != "":
                break
        
        adj1, adj2 = [], []
        if id1 in graph:
            adj1 = graph[id1]
        adj1.append(id2)
        graph[id1] = adj1
        if id2 in graph:
            adj2 = graph[id2]
        adj1.append(id1)
        graph[id2] = adj2

        popup.destroy()

    def close():
        popup.destroy()

    label5 = tk.Label(popup, text="")
    label5.place(x=10, y=120)

    button1 = tk.Button(popup, text="确认", command=submit)
    button1.place(x=170, y=140)
    button1.configure(font=("Consolas", 12), width=15, height=1,
                      relief="ridge", bg="lightblue", activebackground="lightcyan")
    button2 = tk.Button(popup, text="取消", command=close)
    button2.place(x=10, y=140)
    button2.configure(font=("Consolas", 12), width=15,
                      height=1, relief="ridge")

    Combo1.bind("<<ComboboxSelected>>", on_select1)
    Combo2.bind("<<ComboboxSelected>>", on_select2)
