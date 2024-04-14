import loggerjava
import os
import re
import json
import copy
import tkinter as tk
from tkinter import simpledialog, messagebox

if __name__ == "__main__":
    pass


# route = r"C:\Users\Administrator\AppData\LocalLow\bitrich\Rail Route\community levels\c6561489-282c-4e95-a084-237969c02e44\\"

def get_text_input(title, prompt, left=False):
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
        root.geometry("500x250")  # 设置窗口大小

        if left:
            label = tk.Label(root, text=prompt, justify='left')
        else:
            label = tk.Label(root, text=prompt, justify='center')
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


def display_nested_structure(obj, prefix='', indent=0):
    lines = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, list):
                # 特别处理嵌套列表，显示为 stop<n> 格式
                lines.append(f"{prefix}{key}:")
                for i, item in enumerate(value):
                    lines.append(f"{prefix}    stop{i}: {item}")
            else:
                lines.append(f"{prefix}{key}: {value}")
    elif isinstance(obj, list):
        # 对于其他列表，简单地显示其内容（如果需要可以进一步格式化）
        lines.append(str(obj))
    else:
        lines.append(str(obj))
    return lines


def display_dict_list(dict_list):
    def on_prev():
        nonlocal index
        index = (index - 1) % len(dict_list)
        update_label()

    def on_exit():
        root.destroy()

    def on_next():
        nonlocal index
        index = (index + 1) % len(dict_list)
        update_label()

    def update_label():
        current_dict = dict_list[index]
        label_text = "\n".join(display_nested_structure(current_dict))
        label.config(text=label_text)

    root = tk.Tk()
    root.geometry("500x250")  # 增加了高度以适应更多内容
    root.title("Rail Route Schedule Editor")

    index = 0

    label = tk.Label(root, wraplength=450, justify=tk.LEFT)  # 增加wraplength以换行显示
    label.pack(pady=20)

    prev_button = tk.Button(root, text="prev", command=on_prev)
    prev_button.pack(side=tk.LEFT, padx=10, pady=10)

    exit_button = tk.Button(root, text="exit", command=on_exit)
    exit_button.pack(side=tk.LEFT, padx=10, pady=10)

    next_button = tk.Button(root, text="next", command=on_next)
    next_button.pack(side=tk.LEFT, padx=10, pady=10)

    update_label()
    root.mainloop()


def str_to_json_station(input_str):
    # 匹配格式中的变量名、名称和轨道编号
    match = re.match(r'# (\w+) = ([\w\d\s]+) \| .*? \| ([\d, ]+)', input_str)

    if not match:
        raise ValueError("输入的格式不正确，请按照 # code = name | MayBeInitial | track 的格式输入")

        # 提取匹配到的值
    code = match.group(1)
    name = match.group(2)
    track = match.group(3).strip()  # 提取最后一个|后的track数据

    # 转换为JSON格式的字符串
    data = {"name": name, "code": code, "track": track}
    # json_str = json.dumps(data, ensure_ascii=False, indent=4)

    return data


def find_name_by_code(stations, code, type):
    for station in stations:
        if station['code'] == code:
            if type == 1:
                return station['name']
            elif type == 2:
                return station
            elif type == 3:
                return station['track']
    return None

def validate_time(time_str):
    try:
        datetime.strptime(time_str, '%H:%M:%S')
        return True
    except ValueError:
        return False

def search_train(train, trainnum):
    passed = False
    for trains in train:
        if trains['train'] == trainnum:
            passed = True
            logger.debug("train test failed.")
        else:
            passed = False
    return passed


def str_to_json_stops(stop_str):
    # 分割站点信息，并去除空格
    stops_info = stop_str.strip().split()

    # 初始化一个列表来保存所有站点的字典
    stops_list = []

    # 遍历每个站点信息
    for stop_info in stops_info:
        # 分割站点信息的各个字段
        code, track, time_arrive, time_stop = stop_info.split('#')

        # 提取到达时间和停留时间

        # 将提取的信息保存到字典中
        stop_dict = {
            "stationcode": code,
            "stoptrack": int(track),
            "arrivetime": time_arrive,
            "stoptime": int(time_stop)
        }

        # 将站点字典添加到列表中
        stops_list.append(stop_dict)

        # 返回包含所有站点信息的列表
    return stops_list


def str_to_json_train(input_str):
    # 分割火车信息和站点信息
    train_info_str, stops_str = input_str.split(':', 1)

    # 分割train_info中的两个部分（使用'|'）
    train_parts = train_info_str.strip().split('|')

    # 提取train字段
    train_number = train_parts[0]
    train_type_speed_etc = train_parts[1]

    # 提取train_type_speed_etc中的信息（假设格式固定）
    match = re.match(r'(\w+) (\w+) (\d+) (\w+) (\w+)', train_type_speed_etc)
    if not match:
        raise ValueError("火车类型、速度等信息格式不正确")

        # 提取火车类型、速度等信息
    train_number += "|" + match.group(1)
    train_type = match.group(2)
    speedmax = match.group(3)
    composition = match.group(4)
    flags = match.group(5)

    # 调用第二个函数处理站点信息
    stops = str_to_json_stops(stops_str)

    # 构建并返回最终的JSON格式数据
    train_json = {
        "train": train_number,
        "type": train_type,
        "speedmax": speedmax,
        "composition": composition,
        "flags": flags,
        "stops": stops
    }
    return train_json


def json_to_str_train(train_json):
    # 提取火车编号
    train_number = train_json["train"]

    # 提取火车类型、速度等信息，并构建train_type_speed_etc字符串
    train_type = train_json["type"]
    speedmax = train_json["speedmax"]
    composition = train_json["composition"]
    flags = train_json["flags"]
    # 假设火车类型、速度等信息应该按照特定的格式拼接
    train_type_speed_etc = f"{train_type} {speedmax} {composition} {flags}"

    # 构建train_info字符串
    train_info = f"{train_number} {train_type_speed_etc}"

    # 构建站点信息字符串
    stops_str = " ".join(
        f"{stop['stationcode']}#{stop['stoptrack']}#{stop['arrivetime']}#{stop['stoptime']}" for stop in
        train_json["stops"])

    # 组合最终的字符串
    final_str = f"{train_info} : {stops_str}"

    return final_str



logger = loggerjava
# route = input("txt route(the folder route contains the trains.txt,last char should be \ ):")
route = get_text_input("Rail Route Schedule Editor",
                       'the folder route contains the trains.txt,last char should be "\" \nthe trains.txt route:')

logger.clearcurrentlog()
logger.config(showinconsole=False, name="rail_route_schedule_editor_log")
try:
    f = open(route + "trains.txt", mode="r", encoding="UTF-8")
    logger.debug("Opening file:" + route + "trains.txt")
    lines = f.readlines()
    f.close()

except Exception as E:
    logger.warn(loggerjava.exceptionhandler.handler(E), showinconsole=True)
    os.system("pause")
    exit(5)

with open(route + "trains.txt", mode="r", encoding="UTF-8") as f:
    linessss = f.read()
    with open(route + "trains_backup.txt", mode="w", encoding="UTF-8") as f2:
        f2.write(linessss)
logger.debug("Created backup file:" + route + "trains_backup.txt")
stations = []
trains = []
for i in range(5, len(lines)):
    try:
        stations.append(str_to_json_station(lines[i]))
    except ValueError:
        linestop = i
        break
# print(stations)
# logger.debug("showing read stations")
# print("read stations:")
# for i in stations:
#    print("name:%s\ncode:%s\ntrack:%s\n\n" % (i["name"], i["code"], i["track"]))
#    logger.debug("name:%s code:%s track:%s" % (i["name"], i["code"], i["track"]))

original_txt = copy.deepcopy(lines)
original_txt2 = original_txt[:linestop + 22]
original_txt3 = [item.rstrip('\n') for item in original_txt2]
for i in range(linestop + 22, len(lines)):
    trains.append(str_to_json_train(lines[i]))
# logger.debug("showing read trains")
# print("read trains:")
# for i in trains:
#    print("trainnum:%s\ntraintype:%s\nspeedlimit:%s\ncomposition:%s\nflags:%s\n\nstops:" % (
#        i['train'], i['type'], i['speedmax'], i['composition'], i['flags']))
#    logger.debug("train:" + str(i))
#    for j in i["stops"]:
#        print("stop station:%s\nstoptrack:%s\narrivetime:%s\nstoptime:%smin\n" % (
#            find_name_by_code(stations, j["stationcode"], 1), j['stoptrack'], j['arrivetime'], j['stoptime']))
#    print("\n")


# main add train
while 1:
    # num = input("add a train(0 to exit),input the train num(contains |, like C114|C114):")
    choice = get_radio_selection("Rail Route Schedule Editor", 'choose the function:',
                                 ['show trains', 'show stations', 'add a new train', 'exit'])
    if choice == 0:
        display_dict_list(trains)
        continue
    elif choice == 1:
        display_dict_list(stations)
        continue
    elif choice == 3:
        break
    else:
        pass
    num = get_text_input("Rail Route Schedule Editor", 'input the train num(contains |, like C114|C114):')
    if not search_train(trains, num):
        pass
    else:
        messagebox.showerror("Rail Route Schedule Editor", 'Train Number Exists!')
        logger.warn("train num exists:" + num)
        continue
    # train type
    radio_options = ["COMMUTER", "FREIGHT", "IC", "URBAN"]
    type = get_radio_selection("Rail Route Schedule Editor", "choose train type:", radio_options)
    # spdmax
    spdmax = get_number_input("Rail Route Schedule Editor", "speed limit:")
    typee = radio_options[type]

    # composition
    while True:
        composition = get_text_input("Rail Route Schedule Editor", "TrainComposition format:\n"
                                                                   'vvv...\n'
                                                                   'Each v represents one vehicle. \n'
                                                                   'L = locomotive (or control post), C = cargo car, P = passenger car\n'
                                                                   'train composition:', left=True)
        notpass = False
        for f in composition:
            if f not in ['L', 'C', 'P']:
                notpass = True
        if not notpass:
            break
        else:
            messagebox.showerror("Rail Route Schedule Editor", 'error composition format!')

    # flags
    while True:
        flags = get_text_input("Rail Route Schedule Editor", "Flags format:\n"
                                                             'ff\n'
                                                             'Each f is one flag. 0 = flag not set, 1 = flag set, X = position not used\n'
                                                             'Flag positions:\n'
                                                             '#1 unused (X)\n'
                                                             '#2 NoBrakingPenalization - if set (1), train does NOT receive\n'
                                                             ' penalization when braking at signals\n'
                                                             'flags:', left=True)
        notpass = False
        for f in flags:
            if f not in ['X', '0', '1']:
                notpass = True
        if not notpass:
            break
        else:
            messagebox.showerror("Rail Route Schedule Editor", 'error flag format!')
    for i in stations:
        print("name:%s\ncode:%s\ntrack:%s\n\n" % (i["name"], i["code"], i["track"]))
        stops = []
    while 1:
        staioncode = input("the stop station's code(input exit to exit):")
        if staioncode == "exit":
            break
        try:
            stoptrack = int(input("the track train stops(0 for any track):"))
            arrivetime = input("the time train arrives the station(format:hh:mm:ss):")
            stoptime = int(input("the time train stops(in minutes):"))
        except Exception as E:
            print("invaid input")
            logger.warn(loggerjava.exceptionhandler.handler(E))
            continue
        stops.append(
            {'stationcode': staioncode, 'stoptrack': stoptrack, 'arrivetime': arrivetime, 'stoptime': stoptime})
    trains.append(
        {'train': num, 'type': typee, 'speedmax': spdmax, 'composition': composition, 'flags': flags, 'stops': stops})
    logger.debug(
        "Added train:" + {'train': num, 'type': typee, 'speedmax': spdmax, 'composition': composition, 'flags': flags,
                          'stops': stops})
logger.debug("Writing to file:" + route + "trains.txt")
for i in trains:
    original_txt3.append(json_to_str_train(i))
    with open(route + "trains.txt", mode="w", encoding="UTF-8") as f:
        f.write("\n".join(original_txt3))
os.system("pause")
