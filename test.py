if __name__ == "__main__":
    pass
import tkinter as tk
from tkinter import simpledialog, messagebox


# 创建对话框并返回文本输入框的值
def get_text_input(title, prompt):
    while True:
        result = None

        def on_ok():
            nonlocal result
            result = entry.get()
            root.destroy()

        def on_cancel():
            root.destroy()

        root = tk.Tk()
        root.title(title)
        root.geometry("300x150")  # 设置窗口大小

        label = tk.Label(root, text=prompt)
        label.pack(pady=10)

        entry = tk.Entry(root)
        entry.pack(pady=5)

        ok_btn = tk.Button(root, text="OK", command=on_ok)
        ok_btn.pack(side=tk.RIGHT, padx=5, pady=5)

        cancel_btn = tk.Button(root, text="Cancel", command=on_cancel)
        cancel_btn.pack(side=tk.RIGHT, padx=5, pady=5)

        root.grab_set()  # 确保模态对话框行为
        root.transient(root.master)  # 确保对话框与主窗口关联
        root.wait_window(root)  # 等待窗口关闭
        if result is not None and result != "":
            return result


def get_radio_selection(title, prompt, options):
    # 创建主窗口
    root = tk.Tk()
    root.title(title)
    root.geometry(f"500x300")

    # 窗口内的文字提示
    tk.Label(root, text=prompt).pack(pady=20)

    # 初始化变量，用于存储选中的按钮索引
    var = tk.StringVar()
    var.set("")  # 初始设置为空字符串

    # 创建一个Frame用于放置按钮，并设置居中
    button_frame = tk.Frame(root)
    button_frame.pack(pady=50, expand=True)  # 设置垂直间距并允许扩展

    # 创建一组水平排列的按钮
    buttons = []
    for i, option in enumerate(options):
        def on_button_click(index):
            var.set(str(index))  # 设置选中的按钮索引
            root.destroy()  # 销毁窗口

        # 使用lambda和默认参数来捕获当前的i值
        btn = tk.Button(button_frame, text=option, command=lambda idx=i: on_button_click(idx))
        buttons.append(btn)

        # 将按钮水平排列，并添加一些间距
        btn.pack(side=tk.LEFT, padx=5, pady=50)

    # 运行窗口
    root.mainloop()

    # 返回选中的按钮索引，如果窗口被正常关闭而不是通过按钮点击，则返回None
    selected_index = int(var.get()) if var.get().isdigit() else None
    return selected_index


# 创建对话框并返回数字输入框的值
def get_number_input(title, prompt):
    result = None
    while True:
        def on_ok():
            nonlocal result
            try:
                result = int(entry.get())
                root.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number.")

        def on_cancel():
            root.destroy()

        root = tk.Tk()
        root.title(title)
        root.geometry("300x150")  # 设置窗口大小

        label = tk.Label(root, text=prompt)
        label.pack(pady=10)

        entry = tk.Entry(root)
        entry.pack(pady=5)

        ok_btn = tk.Button(root, text="OK", command=on_ok)
        ok_btn.pack(side=tk.RIGHT, padx=5, pady=5)

        cancel_btn = tk.Button(root, text="Cancel", command=on_cancel)
        cancel_btn.pack(side=tk.RIGHT, padx=5, pady=5)

        root.grab_set()  # 确保模态对话框行为
        root.transient(root.master)  # 确保对话框与主窗口关联
        root.wait_window(root)  # 等待窗口关闭

        if result is not None:
            return result

            # 理论上，如果while循环结束，result应该已经被赋值了
    # 但为了代码的完整性，这里返回一个默认值或抛出一个异常
    raise ValueError("No valid number entered.")

    # 主程序入口


def main():
    # 调用函数获取文本输入
    text_value = get_text_input("Rail Route Schedule Editor", "input some text:")
    print(f"text：{text_value}")

    # 调用函数获取单选选择
    radio_options = ["COMMUTER", "FREIGHT", "IC", "URBAN"]
    # train type(1:COMMUTER 2:FREIGHT 3:IC 4:URBAN):
    radio_value = get_radio_selection("Rail Route Schedule Editor", "choose train type:", radio_options)
    print(f"choice：{radio_value}")

    # 调用函数获取数字输入
    num_value = get_number_input("数字输入", "请输入一个数字:")
    print(f"数字输入：{num_value}")
    print(radio_options[radio_value])


if __name__ == "__main__":
    main()
