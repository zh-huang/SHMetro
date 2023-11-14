# 2153689

from heapsort.visual import Visualizer
from heapsort.draw import Button, Label, Input
from heapsort.tools import insert_newlines, is_numeric, coordinate_calculate


import random


class heapSort:
    def __init__(self, dir) -> None:
        self.dir = dir
    
    def init(self):
        self.visualizer = Visualizer(self.dir)
        self.Label0 = Label(self.visualizer.root)
        self.Label1 = Label(self.visualizer.root)
        self.Input = Input(self.visualizer.root)
        self.Button1 = Button(self.visualizer.root)
        self.Button2 = Button(self.visualizer.root)
        self.Button3 = Button(self.visualizer.root)
        self.Button4 = Button(self.visualizer.root)
        
        self.array = []
        self.size_limit = [5, 31]
        self.num_limit = [1, 100]
        self.label_length = 20
        self.temp_array = []
        self.timer = 0
        self.state = 0

    def show_array(self, text, clear=0):
        if clear == 1:
            self.Label0.display_label("", 10, 90, self.label_length, 8)
            return
        text = f"{text}{self.array}"
        text = insert_newlines(text, self.label_length - 2)
        self.Label0.display_label(text, 10, 90, self.label_length, 8)

    def ramdom_generate(self):
        self.array = []
        array_size = random.randint(self.size_limit[0], self.size_limit[1])
        self.array = [random.randint(
            self.num_limit[0], self.num_limit[1]) for _ in range(array_size)]
        self.show_array("生成的数组：")

    def get_input(self):
        input_text = self.Input.text.get("1.0", "end-1c")
        input_array = input_text.split()
        # Ensure numeric
        input_number = []
        for item in input_array:
            if is_numeric(item):
                input_number.append(int(item))
        self.array = input_number
        self.show_array("输入的数组：")
    
    def clear(self):
        self.visualizer.clear()
        self.array = []
        self.temp_array = []
        self.show_array("", 1)
        self.state = 0
        self.timer = 0
        self.Button3.button.config(text="排序", bg="lightblue", activebackground="lightcyan", command=self.heap_sort)

    def draw_points(self):
        for item in self.temp_array:
            tmp_id = self.visualizer.root.after(
                self.timer + 100 * item[1], self.visualizer.draw_circle, item[2], item[3], item[0])
            self.visualizer.afters.append(tmp_id)
        self.timer = self.timer + 100 * len(self.temp_array)
        for i in range(len(self.temp_array) - 1, 0, -1):
            tmp_id = self.visualizer.root.after(
                self.timer, self.visualizer.connect_circles, i, int((i - 1) / 2))
            self.visualizer.afters.append(tmp_id)

    def heapify(self, n, i):
        left, right, largest = 2 * i + 1, 2 * i + 2, i

        if left < n:
            if self.temp_array[left] > self.temp_array[largest]:
                largest = left
        if right < n:
            if self.temp_array[right] > self.temp_array[largest]:
                largest = right

        if largest != i:
            self.timer += 2000
            tmp_id = self.visualizer.root.after(
                self.timer, self.visualizer.swap_circles, self.temp_array[largest][1], self.temp_array[i][1])
            self.visualizer.afters.append(tmp_id)
            self.temp_array[largest], self.temp_array[i] = self.temp_array[i], self.temp_array[largest]
            self.heapify(n, largest)

    def heap_sort(self):
        if self.state != 0 or len(self.array) == 0:
            return
        self.state = 1
        self.Button3.button.config(text="清除", bg="red", activebackground="pink", command=self.clear)
        
        self.temp_array = coordinate_calculate(
            self.array, len(self.array), 200, 800, 0, 600)
        self.draw_points()

        for i in range(int(len(self.temp_array) / 2 - 1), -1, -1):
            self.heapify(len(self.temp_array), i)

        for i in range(len(self.temp_array) - 1, 0, -1):

            self.timer += 2000
            tmp_id = self.visualizer.root.after(
                self.timer, self.visualizer.swap_circles, self.temp_array[0][1], self.temp_array[i][1])
            self.visualizer.afters.append(tmp_id)
            self.temp_array[0], self.temp_array[i] = self.temp_array[i], self.temp_array[0]

            self.timer += 2000
            tmp_id = self.visualizer.root.after(
                self.timer, self.visualizer.change_color, self.temp_array[i][1], "green")
            self.visualizer.afters.append(tmp_id)

            self.heapify(i, 0)

        self.timer += 2000
        tmp_id = self.visualizer.root.after(
            self.timer, self.visualizer.change_color, self.temp_array[0][1], "green")
        self.visualizer.afters.append(tmp_id)

        self.timer += 2000
        self.array = [i[0] for i in self.temp_array]
        tmp_id = self.visualizer.root.after(
            self.timer, self.show_array, "排序后的数组")
        self.visualizer.afters.append(tmp_id)

    def draw_main_window(self):
        self.init()

        self.visualizer.root.title("堆排序可视化")

        self.Button1.draw(10, 20, self.label_length,
                         2, "生成数组", "lightblue", "lightcyan", self.ramdom_generate)

        self.Button2.draw(10, 390, self.label_length,
                         2, "确认", "lightblue", "lightcyan", self.get_input)

        self.Button3.draw(10, 460, self.label_length,
                         2, "排序", "lightblue", "lightcyan", self.heap_sort)

        self.Button4.draw(10, 530, self.label_length,
                         2, "关闭窗口", "red", "pink", self.visualizer.close_canvas)

        self.Label0.display_label("", 10, 90, self.label_length, 7)
        self.Label1.display_label("输入排序数组", 10, 250, self.label_length, 1)
        self.Input.draw_input(10, 280, self.label_length, 4)

        self.visualizer.run()
