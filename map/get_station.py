import json
import requests


def update(dir):
    headers = {'Accept-Language': 'zh-CN,zh;q=0.9'}
    url = 'http://map.amap.com/service/subway?srhdata=3100_drw_shanghai.json'
    response = requests.get(url, headers=headers)
    result = json.loads(response.text)
    stations = []
    for i in result['l']:
        station = []
        for a in i['st']:
            station.append([float(b) for b in a['sl'].split(',')])
        stations.append(station)
    with open(dir, 'w') as file:
        json.dump(result, file, indent=4)


def get_lines(dir):
    with open(dir, 'r') as file:
        data = json.load(file)

    lines = []
    for items in data["l"]:
        line = []
        stations = []
        
        for item in items["st"]:
            latlon = str(item["sl"]).split(',')
            station = [item["sid"], item["n"], bool(int(item["t"])), float(latlon[0]), float(latlon[1])]
            stations.append(station)
        
        k, K = 1, True
        while K:
            K = False
            if k != 1:
                tmpl = items["kn"] + str(k)
            else:
                tmpl = items["kn"]
            for index in lines:
                if tmpl == index[1]:
                    k += 1
                    K = True
                    break
        
        if k == 1:
            line = [items["ln"], items["kn"], items["cl"]]
        else:
            line = [items["ln"] + str(k), items["kn"] + str(k), items["cl"]]
        line.append(stations)
        lines.append(line)
        
    line = ["自定义", "自定义", "black", []]
    lines.append(line)
    return lines
