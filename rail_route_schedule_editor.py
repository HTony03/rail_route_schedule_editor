import loggerjava
import os
import re
import json
import copy

if __name__ == "__main__":
    pass

logger = loggerjava
route = input("txt route(the folder route contains the trains.txt,last char should be \):")
#route = r"C:\Users\Administrator\AppData\LocalLow\bitrich\Rail Route\community levels\c6561489-282c-4e95-a084-237969c02e44\\"


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

    # r'# (\w+) = (\w+ \d+)\ | .*?\ | (\d+, \d+)$'
    # r'# (\w+) = (\w+ \d+)\ | .*? \ | ([\d+,]+)'
    # r'# (\w+) = ([\w\d\s]+) \| .*? \| ([\d,]+)'


def find_name_by_code(stations, code, type):
    for station in stations:
        if station['code'] == code:
            if type == 1:
                return station['name']
            elif type == 2:
                return station
    return None


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
        # arrivetime = time_stop[:8]
        # stoptime = int(time_stop[-1])

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


logger.clearcurrentlog()
logger.config(showinconsole=False,name="rail_route_schedule_editor_log")
try:
    f = open(route + "trains.txt", mode="r", encoding="UTF-8")
    logger.debug("Opening file:" + route + "trains.txt")
    lines = f.readlines()
    f.close()

except Exception as E:
    logger.warn(loggerjava.exceptionhandler.handler(E),showinconsole=True)
    os.system("pause")
    exit(5)

with open(route + "trains.txt", mode="r", encoding="UTF-8") as f:
    linessss = f.read()
    with open(route + "trains_backup.txt", mode="w", encoding="UTF-8") as f2:
        f2.write(linessss)
logger.debug("Created backup file:" + route + "trains_backup.txt")
# for i in lines:
#    print(i)
stations = []
trains = []

for i in range(5, len(lines)):
    try:
        # print(lines[i])
        stations.append(str_to_json_station(lines[i]))
    except ValueError:
        linestop = i
        #print(linestop)
        break
# print(stations)
logger.debug("showing read stations")
print("read stations:")
for i in stations:
    print("name:%s\ncode:%s\ntrack:%s\n\n" % (i["name"], i["code"], i["track"]))
    logger.debug("name:%s code:%s track:%s" % (i["name"], i["code"], i["track"]))


original_txt = copy.deepcopy(lines)
original_txt2 = original_txt[:linestop + 22]
original_txt3 = [item.rstrip('\n') for item in original_txt2]
# for s in original_txt2:
# print(s)
for i in range(linestop + 22, len(lines)):
    # print(lines[i])
    trains.append(str_to_json_train(lines[i]))
logger.debug("showing read trains")
print("read trains:")
for i in trains:
    #print(i)
    print("trainnum:%s\ntraintype:%s\nspeedlimit:%s\ncomposition:%s\nflags:%s\n\nstops:" % (
        i['train'], i['type'], i['speedmax'], i['composition'], i['flags']))
    logger.debug("train:"+str(i))
    for j in i["stops"]:
        print("stop station:%s\nstoptrack:%s\narrivetime:%s\nstoptime:%smin\n" % (
            find_name_by_code(stations, j["stationcode"], 1), j['stoptrack'], j['arrivetime'], j['stoptime']))
    print("\n")


# for i in trains:
#    print(json_to_str_train(i))

while 1:
    num = input("add a train(0 to exit),input the train num(contains |, like C114|C114):")
    if num == "0":
        break
    else:
        pass
    if not search_train(trains, num):
        pass
    else:
        print("train num exists")
        logger.warn("train num exists:"+num)
        continue
    try:
        type = int(input("train type(1:COMMUTER 2:FREIGHT 3:IC 4:URBAN):"))
        spdmax = int(input("speed limit:"))
    except Exception as E:
        print("invaid input")
        logger.warn(loggerjava.exceptionhandler.handler(E))
        continue
    if type == 1:
        typee = "COMMUTER"
    elif type == 2:
        typee = "FREIGHT"
    elif type == 3:
        typee = "IC"
    elif type == 4:
        typee = "URBAN"
    else:
        print("invaid input")
        continue
    print("""TrainComposition format:
vvv...
Each v represents one vehicle. 
L = locomotive (or control post), C = cargo car, P = passenger car""")
    composition = input("train composition:")
    print("""Flags format:
ff
Each f is one flag. 0 = flag not set, 1 = flag set, X = position not used
Flag positions:
#1 unused (X)
#2 NoBrakingPenalization - if set (1), train does NOT receive penalization when braking at signals
    """)
    flags = input("flags:")
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
    logger.debug("Added train:"+{'train': num, 'type': typee, 'speedmax': spdmax, 'composition': composition, 'flags': flags, 'stops': stops})
logger.debug("Writing to file:"+route+"trains.txt")
for i in trains:
    original_txt3.append(json_to_str_train(i))
    with open(route + "trains.txt", mode="w", encoding="UTF-8") as f:
        f.write("\n".join(original_txt3))
os.system("pause")