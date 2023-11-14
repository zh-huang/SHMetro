# 2153689

from map.affine import Affine

import tkinter as tk
RADIUS = 4
SCALE = 0.1


def draw_stations(root: tk.Canvas, stations, Ax: Affine, Ay: Affine, points):
    for station in stations:
        sid, sname, tra, lat, lon = station
        L = True
        if tra == True:
            for lesta in points:
                if lesta[4] == sname:
                    newsta = [lesta[0], lesta[1],
                              lesta[2], str(sid), str(sname)]
                    points.append(newsta)
                    L = False
                    break
        if L:
            x, y = Ax.Forward(float(lat)), Ay.Forward(float(lon))
            nid = root.create_oval(
                x - RADIUS, y - RADIUS, x + RADIUS, y + RADIUS, fill="white", outline="gray", width=2)
            points.append([nid, x, y, str(sid), str(sname)])
    return points


def draw_lines(root: tk.Canvas, lines, Ax: Affine, Ay: Affine):
    points = []
    lsegs = []
    for line in lines:
        name, sname, color, stations = line
        points = draw_stations(root, stations, Ax, Ay, points)
        color = '#' + color
        for index in range(1, len(stations)):
            x1, x2 = stations[index - 1][3], stations[index][3]
            y1, y2 = stations[index - 1][4], stations[index][4]
            x1, y1 = Ax.Forward(float(x1)), Ay.Forward(float(y1))
            x2, y2 = Ax.Forward(float(x2)), Ay.Forward(float(y2))
            line = root.create_line(x1, y1, x2, y2, fill=color)
            root.tag_lower(line)
            lsegs.append([line, x1, y1, x2, y2])
    return points, lsegs


def draw_paths(root: tk.Canvas, points, start, end, paths):
    index1, index2 = -1, -1
    for point in points:
        if start == point[3]:
            index1 = point
            break
    for point in points:
        if end == point[3]:
            index2 = point
            break
    path = root.create_line(
        index1[1], index1[2], index2[1], index2[2], fill="red", width=4)
    root.tag_lower(path)
    paths.append([path, index1[1], index1[2], index2[1], index2[2]])
    return paths


def clear_paths(root: tk.Canvas, paths):
    for path in paths:
        root.delete(path[0])
    paths = []
    return paths


def zoom_in(root: tk.Canvas, points, lsegs, paths, x, y):
    for i in range(len(points)):
        nx = (points[i][1] - x) * (1 + SCALE) + x
        ny = (points[i][2] - y) * (1 + SCALE) + y
        points[i][1] = nx
        points[i][2] = ny
        root.coords(
            points[i][0], nx - RADIUS, ny - RADIUS, nx + RADIUS, ny + RADIUS)
        
    for i in range(len(lsegs)):
        nx1, ny1, nx2, ny2 = lsegs[i][1], lsegs[i][2], lsegs[i][3], lsegs[i][4]
        nx1, nx2 = (nx1 - x) * (1 + SCALE) + x, (nx2 - x) * (1 + SCALE) + x
        ny1, ny2 = (ny1 - y) * (1 + SCALE) + y, (ny2 - y) * (1 + SCALE) + y
        lsegs[i][1], lsegs[i][2], lsegs[i][3], lsegs[i][4] = nx1, ny1, nx2, ny2
        root.coords(lsegs[i][0], nx1, ny1, nx2, ny2)
        
    for i in range(len(paths)):
        nx1, ny1, nx2, ny2 = paths[i][1], paths[i][2], paths[i][3], paths[i][4]
        nx1, nx2 = (nx1 - x) * (1 + SCALE) + x, (nx2 - x) * (1 + SCALE) + x
        ny1, ny2 = (ny1 - y) * (1 + SCALE) + y, (ny2 - y) * (1 + SCALE) + y
        paths[i][1], paths[i][2], paths[i][3], paths[i][4] = nx1, ny1, nx2, ny2
        root.coords(paths[i][0], nx1, ny1, nx2, ny2)


def zoom_out(root: tk.Canvas, points, lsegs, paths, x, y):
    for i in range(len(points)):
        nx = (points[i][1] - x) / (1 + SCALE) + x
        ny = (points[i][2] - y) / (1 + SCALE) + y
        points[i][1] = nx
        points[i][2] = ny
        root.coords(
            points[i][0], nx - RADIUS, ny - RADIUS, nx + RADIUS, ny + RADIUS)
        
    for i in range(len(lsegs)):
        nx1, ny1, nx2, ny2 = lsegs[i][1], lsegs[i][2], lsegs[i][3], lsegs[i][4]
        nx1, nx2 = (nx1 - x) / (1 + SCALE) + x, (nx2 - x) / (1 + SCALE) + x
        ny1, ny2 = (ny1 - y) / (1 + SCALE) + y, (ny2 - y) / (1 + SCALE) + y
        lsegs[i][1], lsegs[i][2], lsegs[i][3], lsegs[i][4] = nx1, ny1, nx2, ny2
        root.coords(lsegs[i][0], nx1, ny1, nx2, ny2)
        
    for i in range(len(paths)):
        nx1, ny1, nx2, ny2 = paths[i][1], paths[i][2], paths[i][3], paths[i][4]
        nx1, nx2 = (nx1 - x) / (1 + SCALE) + x, (nx2 - x) / (1 + SCALE) + x
        ny1, ny2 = (ny1 - y) / (1 + SCALE) + y, (ny2 - y) / (1 + SCALE) + y
        paths[i][1], paths[i][2], paths[i][3], paths[i][4] = nx1, ny1, nx2, ny2
        root.coords(paths[i][0], nx1, ny1, nx2, ny2)
