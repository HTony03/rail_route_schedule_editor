import configparser
import json
import os
import re
import tkinter as tk
from tkinter import messagebox

import loggerjava as logger

if __name__ == "__main__":
    pass

# "C:\Users\Administrator\AppData\LocalLow\bitrich\Rail Route\community levels\c6561489-282c-4e95-a084-237969c02e44\\"
# route = input("txt route(the folder route contains the trains.txt,last char should be \ ):")
logger.config(showinconsole=True, name="rail_route_schedule_editor_log")
logger.clearcurrentlog()
try:
    def get_text_input(title, prompt, left=False, checkclose=False, returnn=False):
        while True:
            result = None
            exiting = False

            def on_ok():
                nonlocal result
                result = entry.get()
                root.destroy()

            def on_cancel():
                nonlocal exiting
                if checkclose:

                    if messagebox.askokcancel(translations['tkinter.confirm'], translations['tkinter.exitinfo']):
                        root.destroy()
                        exiting = True
                    else:
                        pass
                elif returnn:
                    if messagebox.askokcancel(translations['tkinter.confirm'], translations['tkinter.returninfo']):
                        root.destroy()
                        exiting = True
                    else:
                        pass
                else:
                    root.destroy()

            def enterpress(event):
                ok_btn.invoke()

            root = tk.Tk()
            root.title(title)
            root.geometry("500x250")
            root.protocol("WM_DELETE_WINDOW", on_cancel)

            if left:
                label = tk.Label(root, text=prompt, justify='left')
            else:
                label = tk.Label(root, text=prompt, justify='center')
            label.pack(pady=10)

            entry = tk.Entry(root)
            entry.pack(pady=5)

            button_frame = tk.Frame(root)
            button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)  # 放置在底部，并水平填充

            ok_btn = tk.Button(button_frame, text=translations['tkinter.ok'], command=on_ok)
            cancel_btn = tk.Button(button_frame, text=translations['tkinter.cancel'], command=on_cancel)

            button_frame.columnconfigure(0, weight=1)  # 创建一个权重为1的列
            button_frame.columnconfigure(1, weight=1)  # 创建一个权重为1的列

            # 使用grid布局将按钮放置在button_frame中，并确保它们居中
            ok_btn.grid(row=0, column=0, padx=10, pady=5)
            cancel_btn.grid(row=0, column=1, padx=10, pady=5)

            # 确保button_frame中的列均匀分布
            for i in range(2):
                button_frame.grid_columnconfigure(i, weight=1)

            entry.bind("<Return>", enterpress)

            root.grab_set()  # 确保模态对话框行为
            root.transient(root.master)  # 确保对话框与主窗口关联
            root.wait_window(root)  # 等待窗口关闭
            if result is not None and result != "":
                return result
            if exiting and checkclose:
                logger.info("selected close, exit program")
                os._exit(0)
                return "-1"
            if returnn and exiting:
                return "-1"
        return -1


    def get_radio_selection(title, prompt, options, returns=False):
        def enterperss():
            if returns:
                btn.invoke()

        def calculate_columnspan(index, total_buttons, max_columns=4):
            if total_buttons <= max_columns:
                # 当总数小于等于4时，计算每个按钮的columnspan
                return (index + 1) / (total_buttons + 1)
            else:
                # 当总数大于4时，每行4个按钮
                row = (index + 1) // (max_columns + 2)
                col = index % max_columns
                return 1  # 每个按钮占据一列

        # 创建主窗口
        root = tk.Tk()
        root.title(title)
        root.geometry(f"625x%s" % str(250 + (len(options) // 5 + 1) * 27))

        # 窗口内的文字提示
        tk.Label(root, text=prompt).pack(pady=20)

        # 初始化变量，用于存储选中的按钮索引
        var = tk.StringVar()
        var.set("")  # 初始设置为空字符串

        root.protocol("WM_DELETE_WINDOW", enterperss)

        # 创建一个Frame用于放置按钮，并设置居中
        button_frame = tk.Frame(root)
        button_frame.pack(pady=50, expand=True, fill='x')  # 设置垂直间距并允许扩展
        # button_frame.pack(expand=True, fill='both')

        num_columns = max(len(options), 4) + 2
        for col in range(num_columns):
            button_frame.columnconfigure(col, weight=1)

        button_row = 0
        button_col = 0

        # 创建一组水平排列的按钮
        buttons = []
        for i, option in enumerate(options):
            columnspan = calculate_columnspan(i, len(options))
            if columnspan > 1:
                # 如果columnspan大于1，则合并列
                button_frame.columnconfigure(button_col, minsize=int(root.winfo_width() * columnspan / len(options)))

            def on_button_click(index):
                var.set(str(index))  # 设置选中的按钮索引
                root.destroy()  # 销毁窗口

            # 使用lambda和默认参数来捕获当前的i值
            btn = tk.Button(button_frame, text=option, command=lambda idx=i: on_button_click(idx))
            btn.grid(row=button_row, column=button_col + 1, sticky='ew', padx=5)
            buttons.append(btn)

            if (i + 1) % 4 == 0 or (i + 1) == len(options):
                button_row += 1
                button_col = 0
            else:
                button_col += 1

        # 运行窗口
        root.mainloop()

        # 返回选中的按钮索引，如果窗口被正常关闭而不是通过按钮点击，则返回None
        selected_index = int(var.get()) if var.get().isdigit() else None
        return selected_index


    def get_number_input(title, prompt):
        result = None
        while True:
            def on_ok():
                nonlocal result
                try:
                    result = int(entry.get())
                    root.destroy()
                except ValueError:
                    messagebox.showerror(translations['tkinter.error'], translations['tkinter.invaidnum'])

            def on_cancel():
                root.destroy()

            def enterpress(event):
                ok_btn.invoke()

            root = tk.Tk()
            root.title(title)
            root.geometry("300x150")  # 设置窗口大小
            root.protocol("WM_DELETE_WINDOW", on_cancel)

            label = tk.Label(root, text=prompt)
            label.pack(pady=10)

            entry = tk.Entry(root)
            entry.pack(pady=5)

            ok_btn = tk.Button(root, text=translations['tkinter.ok'], command=on_ok)
            ok_btn.pack(side=tk.RIGHT, padx=5, pady=5)

            cancel_btn = tk.Button(root, text=translations['tkinter.cancel'], command=on_cancel)
            cancel_btn.pack(side=tk.RIGHT, padx=5, pady=5)

            entry.bind("<Return>", enterpress)

            root.grab_set()  # 确保模态对话框行为
            root.transient(root.master)  # 确保对话框与主窗口关联
            root.wait_window(root)  # 等待窗口关闭

            if result is not None:
                return result

                # 理论上，如果while循环结束，result应该已经被赋值了
        # 但为了代码的完整性，这里返回一个默认值或抛出一个异常
        raise ValueError("No valid number entered.")
        return -1


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
        # 增加了高度以适应更多内容
        root.title("Rail Route Schedule Editor")
        root.protocol("WM_DELETE_WINDOW", on_exit)

        index = 0
        root.geometry("550x%s" % str(160 + len(display_nested_structure(dict_list[index])) * 20))
        label = tk.Label(root, wraplength=450, justify=tk.LEFT)  # 增加wraplength以换行显示
        label.pack(pady=20)

        # 创建一个frame来放置按钮，并使用grid布局
        button_frame = tk.Frame(root)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)  # 放置在底部，并水平填充

        prev_button = tk.Button(button_frame, text=translations['tkinter.prev'], command=on_prev)
        exit_button = tk.Button(button_frame, text=translations['tkinter.exit'], command=on_exit)
        next_button = tk.Button(button_frame, text=translations['tkinter.next'], command=on_next)

        button_frame.columnconfigure(0, weight=1)  # 创建一个权重为1的列
        button_frame.columnconfigure(1, weight=1)  # 创建一个权重为1的列（用于间距）
        button_frame.columnconfigure(2, weight=1)  # 创建一个权重为1的列

        # 使用grid布局将按钮放置在button_frame中，并确保它们居中
        prev_button.grid(row=0, column=0, padx=10, pady=5)
        exit_button.grid(row=0, column=1, padx=10, pady=5)  # 这将是中间的按钮
        next_button.grid(row=0, column=2, padx=10, pady=5)

        # 确保button_frame中的列均匀分布
        for i in range(3):
            button_frame.grid_columnconfigure(i, weight=1)

        update_label()
        root.mainloop()


    def sliding_selector(title, prompt, options):
        def on_ok():
            nonlocal selected_index
            selected_index = listbox.curselection()
            if selected_index:
                selected_index = selected_index[0]
                top.destroy()
                return selected_index
            else:
                top.destroy()
                return None

        top = tk.Tk()
        top.title(title)

        selected_index = None

        frame = tk.Frame(top)
        frame.pack(pady=20, padx=20, fill='both', expand=True)

        tk.Label(frame, text=prompt).pack(pady=(0, 10))

        scrollbar = tk.Scrollbar(frame)
        listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, exportselection=False)
        scrollbar.config(command=listbox.yview)

        for idx, option in enumerate(options):
            listbox.insert(tk.END, option)

        listbox.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.pack(side=tk.RIGHT, fill='y')

        ok_button = tk.Button(frame, text="确定", command=on_ok)
        ok_button.pack(pady=10, side=tk.RIGHT)

        top.mainloop()

        # 如果没有选择直接返回None
        return selected_index


    def str_to_json_station(input_str):
        # 匹配格式中的变量名、名称和轨道编号
        match = re.match(r'# (\S+) = ([^|]+) \| (\d+) \| ([\d, ]+)', input_str)

        if not match:
            raise ValueError("输入的格式不正确，请按照 # code = name | MayBeInitial | track 的格式输入")

            # 提取匹配到的值
        code = match.group(1)
        name = match.group(2)
        track = match.group(4).strip()  # 提取最后一个|后的track数据

        data = {"name": name,
                "code": code,
                "track": track}

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
            re.match(time_str, '%H:%M:%S')
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

            # 将提取的信息保存到字典中
            stop_dict = {
                "stationcode": code,
                "stationname": find_name_by_code(stations, code, 1),
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
        train_data = {
            "train": train_number,
            "type": train_type,
            "speedmax": speedmax,
            "composition": composition,
            "flags": flags,
            "stops": stops
        }
        return train_data


    def json_to_str_train(train_data):
        # 提取火车编号
        train_number = train_data["train"]

        # 提取火车类型、速度等信息，并构建train_type_speed_etc字符串
        train_type = train_data["type"]
        speedmax = train_data["speedmax"]
        composition = train_data["composition"]
        flags = train_data["flags"]
        # 假设火车类型、速度等信息应该按照特定的格式拼接
        train_type_speed_etc = f"{train_type} {speedmax} {composition} {flags}"

        # 构建train_info字符串
        train_info = f"{train_number} {train_type_speed_etc}"

        # 构建站点信息字符串
        stops_str = " ".join(
            f"{stop['stationcode']}#{stop['stoptrack']}#{stop['arrivetime']}#{stop['stoptime']}" for stop in
            train_data["stops"])

        # 组合最终的字符串
        final_str = f"{train_info} : {stops_str}"

        return final_str


    def addtrain():
        while True:
            num = get_text_input("Rail Route Schedule Editor",
                                 translations["info.gettrainnum"], returnn=True)
            if num == '-1':
                return
            if not search_train(trains, num):
                break
            else:
                messagebox.showerror("Rail Route Schedule Editor", translations["warning.trainnumexist"]%num)
                logger.warn("train num exists:" + num)
                return
        # train type
        radio_options = eval(translations['selection.traintype'])
        type = get_radio_selection("Rail Route Schedule Editor", translations["info.gettraintype"]%num, radio_options)
        # spdmax
        spdmax = get_number_input("Rail Route Schedule Editor", translations["info.getmaxspd"]%num)
        typee = radio_options[type]

        # composition
        while True:
            composition = get_text_input("Rail Route Schedule Editor",
                                         translations['info.getcomposition.desc1'] +
                                         translations['info.getcomposition.desc2'] +
                                         translations['info.getcomposition.desc3'] +
                                         translations['info.getcomposition.desc4'] +
                                         translations['info.getcomposition']%num
                                         , left=True)
            notpass = False
            for f in composition:
                if f not in ['L', 'C', 'P']:
                    notpass = True
            if composition[0] != "L":
                notpass = True
            if not notpass:
                break
            else:
                messagebox.showerror("Rail Route Schedule Editor",
                                     translations['warning.errformat']%translations['name.composition'])

        # flags
        while True:
            flags = get_text_input("Rail Route Schedule Editor",
                                   translations['info.getflag.desc1'] +
                                   translations['info.getflag.desc2'] +
                                   translations['info.getflag.desc3'] +
                                   translations['info.getflag.desc4'] +
                                   translations['info.getflag.desc5'] +
                                   translations['info.getflag.desc6'] +
                                   translations['info.getflag.desc7'] +
                                   translations['info.getflag']%num, left=True)

            notpass = False
            for f in flags:
                if f not in ['X', '0', '1']:
                    notpass = True
            if flags[0] != 'X':
                notpass = True
            if len(flags) != 2:
                notpass = True
            if not notpass:
                break
            else:
                messagebox.showerror("Rail Route Schedule Editor",
                                     translations['warning.errformat']%translations['name.flag'])

        stops = []
        stopname = []
        stoptrack = []
        for i in stations:
            stopname.append(str(i['name'] + '(' + i['code'] + ')'))
            stoptrack.append(i['track'])
        stopname.append("exit")
        while 1:
            stationselect = sliding_selector('Rail Route Schedule Editor',
                                             translations['info.getstop']%num, stopname)
            if stationselect is None:
                continue

            if stationselect == len(stopname) - 1:
                if len(stops) >= 2:
                    break
                else:
                    messagebox.showerror("Rail Route Schedule Editor", translations['warning.notenoughstops'])
                    continue
            stationcode = stations[stationselect]['code']

            tracks = gettracks(stations[stationselect]['track'])
            tracks.append('0')
            logger.debug('readed tracks:' + str(tracks))
            stoptrack2 = get_radio_selection('Rail Route Schedule Editor', translations['info.getstoptrack'],
                                             tracks)
            stoptrack = tracks[stoptrack2]
            correctformat = False
            while not correctformat:
                arrivetime = get_text_input('Rail Route Schedule Editor',
                                            translations['info.getarrivetime'])
                if validate_time(arrivetime):
                    correctformat = True
                else:
                    messagebox.showerror("Rail Route Schedule Editor",
                                         translations['warning.errformat']% translations['name.time'])
            stoptime = get_number_input('Rail Route Shedule Editor',
                                        translations['info.getstoptime'])

            stops.append(
                {'stationcode': stationcode,
                 'stoptrack': stoptrack,
                 'arrivetime': arrivetime,
                 'stoptime': stoptime})
        trainadd = {'train': num,
                    'type': typee,
                    'speedmax': spdmax,
                    'composition': composition,
                    'flags': flags,
                    'stops': stops}
        logger.debug(
            "Added train:" + str(trainadd))
        trains.append(trainadd)
        # return trainadd


    def gettracks(trackstr):
        pattern = r'\d+'
        # 使用re.findall找到所有匹配项
        matches = re.findall(pattern, trackstr)
        return matches


    def createcfg():
        lang_options = ['Engligh(en_us)', '中文(zh_cn)']
        lang = get_radio_selection("Rail Route Schedule Editor", "Thank you for using this program.\n"
                                                                 "please select your language:", lang_options)
        langg = ["en_us", "zh_cn"]

        config = configparser.ConfigParser()
        config['DEFAULT'] = {'lang': langg[lang]}
        with open('Rail_route_schedule_editor.cfg', 'w') as configfile:
            config.write(configfile)
        return langg[lang]


    logger.register_def(json_to_str_train)
    logger.register_def(str_to_json_train)
    logger.register_def(str_to_json_stops)
    logger.register_def(str_to_json_station)
    logger.register_def(search_train)
    logger.register_def(validate_time)
    logger.register_def(find_name_by_code)
    logger.register_def(display_dict_list)
    logger.register_def(display_nested_structure)
    logger.register_def(get_radio_selection)
    logger.register_def(get_text_input)
    logger.register_def(get_number_input)
    logger.register_def(addtrain)
    logger.register_def(createcfg)
    logger.register_def(sliding_selector)

    # cfg and translation part
    config_path = 'Rail_route_schedule_editor.cfg'
    if os.path.exists(config_path):
        config = configparser.ConfigParser()
        config.read(config_path)
        lang = config['DEFAULT'].get('lang', 'en_us')
    else:
        logger.warn("no config detected,creating a new one")
        lang = createcfg()
    try:
        with open(r'.\\_internal\\translation\\' + lang + '.json', 'r', encoding='utf-8') as f:
            translations = json.load(f)
    except FileNotFoundError as E:
        logger.warn(logger.exceptionhandler.handler(E), showinconsole=True)
        messagebox.showerror('Rail Route Schedule Editor', 'Translation file:\\translation\\' + lang +
                             '.json not exist\n')
        os.system("pause")
        os._exit(5)
    except json.JSONDecodeError as E:
        logger.warn(logger.exceptionhandler.handler(E), showinconsole=True)
        messagebox.showerror('Rail Route Schedule Editor', 'Translation file:\\translation\\' + lang +
                             '.json seems to be broken.\nplease redownload the translation files and replace them')
        os.system("pause")
        os._exit(5)

    # get file location
    route = get_text_input("Rail Route Schedule Editor",
                           translations["main.get_file_location"], checkclose=True)
    try:
        f = open(route + "trains.txt", mode="r", encoding="UTF-8")
        logger.debug("Opening file:" + route + "trains.txt")
        lines = f.readlines()
        f.close()

    except Exception as E:
        logger.warn(logger.exceptionhandler.handler(E), showinconsole=True)
        messagebox.showerror('Rail Route Schedule Editor', translations["main.fileopenerror"].format(route) + str(E))
        os.system("pause")
        os._exit(5)

    with open(route + "trains.txt", mode="r", encoding="UTF-8") as f:
        linessss = f.read()
        with open(route + "trains_backup.txt", mode="w", encoding="UTF-8") as f2:
            f2.write(linessss)
    logger.debug("Created backup file:" + route + "trains_backup.txt")

    "---------------"
    if linessss[0] != "+++stations\n":
        logger.warn("Invaid file readed!")
        messagebox.showerror('Rail Route Schedule Editor', translations["main.fileerror"].format(route) + str(E))
        os.system("pause")
        os._exit(5)

    "-------------------"
    stations = []
    trains = []
    # read stops
    for i in range(5, len(lines)):
        try:
            stations.append(str_to_json_station(lines[i]))
        except ValueError:
            linestop = i
            break

    original_txt = list(lines)
    original_txt2 = original_txt[:linestop + 22]
    original_txt3 = [item.rstrip('\n') for item in original_txt2]
    # read trains
    for i in range(linestop + 22, len(lines)):
        trains.append(str_to_json_train(lines[i]))

    # main sel
    while 1:
        functions = {0:display_dict_list(trains),1:display_dict_list(stations),2:addtrain()}
        choice = get_radio_selection("Rail Route Schedule Editor", translations['main.choosefunc'],
                                     eval(translations['main.funcselection']), returns=True)
        logger.debug("choice:" + eval(translations['main.funcselection'])[choice])
        if choice in functions:
            functions[choice]
        elif choice == 3:
            break
        else:
            pass
    logger.debug("Writing to file:" + route + "trains.txt")
    for i in trains:
        original_txt3.append(json_to_str_train(i))
        with open(route + "trains.txt", mode="w", encoding="UTF-8") as f:
            f.write("\n".join(original_txt3))
    messagebox.showinfo("Rail Route Schedule Editor", translations['main.saveclose'])
    os.system("pause")
    os._exit(0)

except Exception as E:
    logger.error("----------exceptions---------")
    logger.error(logger.handler(E),pos="exceptionhandler")
    logger.error("file read:\n" + str(lines))
    logger.info("current trains:\n" + str(trains))
    logger.info("current stations:\n" + str(stations))
    messagebox.showerror(translations["exceptionhandler.title"], translations['exceptionhandler.msg'])
    os._exit(105)
