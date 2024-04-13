if __name__ == "__main__":
    pass
import tkinter as tk
from tkinter import simpledialog, messagebox

# 创建对话框并返回文本输入框的值
def get_text_input(title, prompt):
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    value = simpledialog.askstring(title, prompt)
    root.destroy()  # 关闭Tkinter窗口
    return value

# 创建对话框并返回单选按钮的值
def get_radio_selection(title, prompt, options):
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    result = simpledialog.askstring(title, prompt, values=options)
    root.destroy()  # 关闭Tkinter窗口
    return result

# 创建对话框并返回数字输入框的值
def get_number_input(title, prompt):
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    result = simpledialog.askfloat(title, prompt)
    root.destroy()  # 关闭Tkinter窗口
    return result

# 主程序入口
def main():
    # 调用函数获取文本输入
    text_value = get_text_input("Rail Route Schedule Editor", "input some text:")
    print(f"text：{text_value}")

    # 调用函数获取单选选择
    radio_options = ["COMMUTER", "FREIGHT", "IC","URBAN"]
    #train type(1:COMMUTER 2:FREIGHT 3:IC 4:URBAN):
    radio_value = get_radio_selection("Rail Route Schedule Editor", "choose train type:", radio_options)
    print(f"choice：{radio_value}")

    # 调用函数获取数字输入
    num_value = get_number_input("数字输入", "请输入一个数字:")
    print(f"数字输入：{num_value}")

if __name__ == "__main__":
    main()
