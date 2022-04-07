# -*- coding: UTF-8 -*-
import json

if __name__ == '__main__':
    mudb_file_path = "D:\\temp\ssr\\mudb.json"
    mudb_file = open(mudb_file_path, mode="r")
    mudb_str = mudb_file.read()
    if mudb_str is None or mudb_str == "":
        print("文件中无内容:" + mudb_file_path)
        mudb_file.close()
    mudb_dumps = json.loads(mudb_str)
    if mudb_dumps is None or mudb_dumps.__len__() < 1:
        print("文件无法格式化为json:")
        print(mudb_str)
        mudb_file.close()
    mudb_file.close()
    print(mudb_str)
    mudb_json = mudb_dumps[0]
    mudb_json["port"] += 1
    print("更新后端口为:" + str(mudb_json["port"]))
    mudb_dumps[0] = mudb_json
    print(mudb_dumps)
    str = json.dumps(mudb_dumps, sort_keys=True, indent=4, separators=(',', ':'))
    print(str)
    mudb_file = open(mudb_file_path, mode="w")
    mudb_file.write(str)
    mudb_file.close()
