# 2153689

from heapsort import heapSort, Visualizer, Button
from map import Metro
import tkinter as tk
import os


def mainWindow(visualizer: Visualizer, heapsort: heapSort, metro: Metro):
    root = visualizer.root
    root.title("2153689 黄泽华 数据结构课程设计")
    
    Button1 = Button(root)
    Button2 = Button(root)
    Button3 = Button(root)
    
    Button1.draw(50, 50, 40, 2, "堆排序可视化", "lightblue", "lightcyan", heapsort.draw_main_window)
    Button2.draw(50, 150, 40, 2, "上海地铁换乘指南", "lightblue", "lightcyan", metro.draw_main_window)
    Button3.draw(50, 250, 40, 2, "关闭窗口", "red", "pink", visualizer.close_canvas)

    visualizer.run()


if __name__ == "__main__":
    dir = os.path.dirname(__file__)
    heapsort = heapSort(dir)
    visualizer = Visualizer(dir, 480, 360)
    metro = Metro(dir)

    mainWindow(visualizer, heapsort, metro)
