# -*- coding: UTF-8 -*-
import git
if __name__ == '__main__':
    # 读取当前目录的Git库
    repo = git.Repo('.')
    branches = repo.branches
    print(str(branches))
    # 创建文件
    file_name = 'test.file'
    with open(file_name, 'w') as fobj:
        fobj.write('1111111111111111111111st line\n')
        fobj.write('1111111111111111111111st line\n')
    repo.index.add(items=[file_name])
    repo.index.commit('write a line into ' + file_name)
    repo.remote().push()
    repo.close()
