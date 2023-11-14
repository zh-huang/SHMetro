import tkinter as tk
from tkinter import simpledialog

# 创建主窗口
root = tk.Tk()
root.title("示例应用")

# 创建弹出窗口函数
def popup_window():
    # 创建新窗口
    popup = tk.Toplevel(root)
    popup.title("弹出窗口")

    # 创建下拉选项框
    options = ["选项1", "选项2", "选项3"]
    option_var = tk.StringVar()
    option_var.set(options[0])
    option_menu = tk.OptionMenu(popup, option_var, *options)
    option_menu.pack()

    # 创建两个输入float的框
    float_entry1 = tk.Entry(popup, text="Float 1")
    float_entry2 = tk.Entry(popup, text="Float 2")
    float_entry1.pack()
    float_entry2.pack()

    # 创建两个输入string的框
    string_entry1 = tk.Entry(popup, text="String 1")
    string_entry2 = tk.Entry(popup, text="String 2")
    string_entry1.pack()
    string_entry2.pack()

    # 创建提交按钮
    def submit():
        selected_option = option_var.get()
        input_float1 = float(float_entry1.get())
        input_float2 = float(float_entry2.get())
        input_string1 = string_entry1.get()
        input_string2 = string_entry2.get()

        # 在这里执行相应的操作，可以在这里处理用户输入的数据

        # 返回值示例（这里仅为示范）
        result = f"选项: {selected_option}, Float1: {input_float1}, Float2: {input_float2}, String1: {input_string1}, String2: {input_string2}"
        simpledialog.messagebox.showinfo("结果", result)

    submit_button = tk.Button(popup, text="提交", command=submit)
    submit_button.pack()

# 创建按钮用于触发弹出窗口
popup_button = tk.Button(root, text="弹出窗口", command=popup_window)
popup_button.pack()

root.mainloop()
