# -*- coding: UTF-8 -*-
import os


if __name__ == '__main__':
    os.system('chcp 65001')
    flag = os.system("ping 123")
    # environ获取系统变量(发现了有部分中文乱码情况，但只是部分乱码，很奇怪)
    data = os.environ
    print(data)
    print(flag)