# -*- coding: UTF-8 -*-

# 1. 修改配置文件 /usr/local/shadowsocksr/mudb.json 中端口
# 2. 停止ssr服务 /etc/init.d/ssrmu stop
# 3. 启动ssr服务 /etc/init.d/ssrmu start
# 4. 生成ssr url，推送到gitee上
import base64
import json
import os
import random
import socket

mudb_file_path = "/usr/local/shadowsocksr/mudb.json"
ssr_stop = "/etc/init.d/ssrmu stop"
ssr_start = "/etc/init.d/ssrmu start"

base_format = "{ip}:{port}:{protocol}:{method}:{obfs}:{passwd_base}/?group={group_base}&remarks={remarks_base}"

url_src = "url_src.txt"
url_base64 = "url_base64.txt"
url_2 = "url_2.txt"

git_commit = 'git commit -am "提交修改"'
git_push = "git push"
git_pull = "git pull"

# 移除旧端口
command_remove_port = "firewalld-cmd --remove-port={port}/tcp"
# 增加新端口
command_add_port = "firewalld-cmd --permanent --add-port={port}/tcp"
# 重新加载配置
command_reload_firewalld = "firewall-cmd --reload"


def update_mudb_port():
    # 首先读取文件，更新端口号
    mudb_file = open(mudb_file_path, mode="r")
    mudb_str = mudb_file.read()
    if mudb_str is None or mudb_str == "":
        print("文件中无内容:" + mudb_file_path)
        mudb_file.close()
        return None
    mudb_dumps = json.loads(mudb_str)
    if mudb_dumps is None or mudb_dumps.__len__() < 1:
        print("文件无法格式化为json:")
        print(mudb_str)
        mudb_file.close()
        return None
    mudb_file.close()
    mudb_json = mudb_dumps[0]
    old_port = mudb_json["port"]
    print("旧后端:" + str(old_port))
    remove_port(str(old_port))
    mudb_json["port"] = get_port()
    print("新端口:" + str(mudb_json["port"]))
    add_port(str(mudb_json["port"]))
    mudb_dumps[0] = mudb_json
    print(mudb_dumps)
    str2 = json.dumps(mudb_dumps, sort_keys=True, indent=4, separators=(',', ':'))
    print(str2)
    mudb_file = open(mudb_file_path, mode="w")
    mudb_file.write(str2)
    mudb_file.close()
    return mudb_dumps


def remove_port(port):
    os.system(command_remove_port.replace("{port}", port))


def add_port(port):
    os.system(command_add_port.replace("{port}", port))
    os.system(command_reload_firewalld)

def str_to_base64(str_):
    return str(base64.urlsafe_b64encode(str_.encode("utf-8")), "utf-8").replace("=", "")
    # return str(base64.b64encode(str_.encode("utf-8")), "utf-8")


def replace_params(mudb_json):
    url = base_format.replace("{ip}", mudb_json["user"]) \
        .replace("{ip}", mudb_json["user"]) \
        .replace("{port}", str(mudb_json["port"])) \
        .replace("{protocol}", mudb_json["protocol"]) \
        .replace("{method}", mudb_json["method"]) \
        .replace("{obfs}", mudb_json["obfs"]) \
        .replace("{passwd_base}", str_to_base64(mudb_json["passwd"])) \
        .replace("{group_base}", str_to_base64("mine")) \
        .replace("{remarks_base}", str_to_base64(mudb_json["protocol_param"]))
    print(url)
    return url


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


def replace_url_src(url_):
    file = open(url_src, mode="r")
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
    else:
        lines[index] = url_
    print(str(lines))
    write_str = "\n".join(lines)
    print(write_str)
    write_file(url_src, write_str)


def base64_url():
    with open(url_src, mode="r") as f:
        src_lines = f.readlines()
        # 循环生成base64
        base64_list = []
        for line in src_lines:
            base64_list.append("ssr://" + str_to_base64(line.replace("\r", "").replace("\n", "")))
        # 写入到base64文件
        write_str = "\n".join(base64_list)
        print(write_str)
        write_file(url_base64, write_str)
        # 写入到最终文件
        result_str = str_to_base64(write_str)
        print(result_str)
        write_file(url_2, result_str)


def get_port():
    port = random.randint(1000, 65535)
    while True:
        flag = check_port_in_use(port=port)
        if not flag:
            break
    return port


def check_port_in_use(port, host='127.0.0.1'):
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((host, int(port)))
        print("当前端口正在使用:" + str(port))
        return True
    except socket.error:
        print("当前端口未使用:" + str(port))
        return False
    finally:
        if s:
            s.close()


if __name__ == '__main__':
    os.system(git_pull)
    os.system(ssr_stop)
    # 更新端口
    mudb_dumps = update_mudb_port()
    if None is not mudb_dumps:
        for mudb_dump in mudb_dumps:
            # 生成url
            url_ = replace_params(mudb_dump)
            # 读取url_src
            replace_url_src(url_)
            # 生成base64编码
            base64_url()
            print("ssr配置文件更新完成")
        # 重启服务
        os.system(ssr_start)
        # 提交git
        os.system(git_commit)
        # 推送到远程
        os.system(git_push)
    else:
        print("ssr配置文件未读取到")

