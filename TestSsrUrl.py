# -*- coding: UTF-8 -*-
# orcl138.onelol.top:48765:auth_aes128_md5:aes-128-ctr:plain:ZG91Yi5pbw/?group=bWluZQ&remarks=55Sy6aqo5paHMTM4IC0g5q2j5bi4
import base64
import json
import time

base_format = "{ip}:{protocol}:{method}:{obfs}:{passwd_base}/?group={group_base}&remarks={remarks_base}"

def str_to_base64(str_):
    return str(base64.urlsafe_b64encode(str_.encode("utf-8")), "utf-8").replace("=", "")
    # return str(base64.b64encode(str_.encode("utf-8")), "utf-8")

def replace_params():
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

    url = base_format.replace("{ip}", mudb_json["user"]) \
        .replace("{ip}", mudb_json["user"]) \
        .replace("{protocol}", mudb_json["protocol"]) \
        .replace("{method}", mudb_json["method"]) \
        .replace("{obfs}", mudb_json["obfs"]) \
        .replace("{passwd_base}", mudb_json["passwd"]) \
        .replace("{group_base}", str_to_base64("mine")) \
        .replace("{remarks_base}", str_to_base64(mudb_json["protocol_param"]))
    print(url)
    return url


def replace_url_src(url_):
    file_path = "url_src.txt"
    file = open(file_path, mode="r")
    lines = file.readlines()
    file.close()
    print(str(lines))
    server = str(url_.split(":")[0])
    index = lines.__len__()
    for i in range(lines.__len__()):
        lines[i] = lines[i].replace("\r", "").replace("\n", "")
        if server.__eq__(str(lines[i].split(":")[0])):
            index = i
    print("替换第" + str(index) + "行数据")
    if index >= lines.__len__():
        lines.append(url_)
    for l in lines:
        l = l.replace("\r", "").replace("\n", "")
    print(str(lines))
    file_path = "url_src_2.txt"
    write_str = "\n".join(lines)
    print(write_str)
    write_file(file_path, write_str)


def write_file(file_path, file_str):
    # 数据备份
    # now = int(round(time.time() * 1000))
    # now02 = time.strftime('%Y%m%d%H%M%S', time.localtime(now / 1000))
    # file_path_bak = file_path + "." + str(now02)
    # with open(file_path, mode="r") as f:
    #     with open(file_path_bak, mode="w") as f2:
    #         f2.write(f.read())
    with open(file_path, mode="w") as f:
        f.write(file_str)

def base64_url():
    with open("url_src_2.txt", mode="r") as f:
        src_lines = f.readlines()
        # 循环生成base64
        base64_list = []
        for line in src_lines:
            base64_list.append("ssr://" + str_to_base64(line.replace("\r", "").replace("\n", "")))
        # 写入到base64文件
        write_str = "\n".join(base64_list)
        print(write_str)
        write_file("url_base64_2.txt", write_str)
        # 写入到最终文件
        result_str = str_to_base64(write_str)
        print(result_str)
        write_file("url_2_2.txt", result_str)

if __name__ == '__main__':


    # write_file("test123.txt", "2222222222222222")
    replace_url_src("bwg.onelol.top:38799:auth_aes128_md5:aes-128-ctr:plain:ZG91Yi5pbw/?group=bWluZQ&remarks=5pCs55Om5belIC0g56iz5a6a")
    base64_url()
    # replace_params()
    # print(str_to_base64("m+==///==in/e"))