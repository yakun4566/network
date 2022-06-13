## 服务器环境
### Oracle服务器，首先切换用户
` sudo su - root `

### 安装minicoda
1. 下载脚本  
` wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh `

2. 安装 miniconda  
```
chmod +x Miniconda3-latest-Linux-x86_64.sh  
./Miniconda3-latest-Linux-x86_64.sh 
```  
一会回车，敲yes
> 重新打开窗口，conda才能生效（每次打开新窗口都需要切换用户 sudo su - root）

### 安装Python
1. 然后再根据环境安装python版本，这里我们安装python3.8  
` conda create -n=python3_8 python=3.8 `  
输入y，回车

2. 切换到python3.8的环境  
` conda activate python3_8 `

## shadowsocksr配置
### 修改ssr配置文件
` vi /usr/local/shadowsocksr/mudb.json `
- 修改user为ip或域名
- 修改protocl_param为备注


## git配置(以前执行过这个步骤可以忽略)
### 生成本地密钥放到github后台
1. 先把本地ssh密钥生成，放到git后台  
` ssh-keygen -t ed25519 -C "yakun4555@qq.com" `  
回车三次

2. 查看生成的公钥  
` cat ~/.ssh/id_ed25519.pub `  
把公钥粘贴到git后台

### 设置git全局用户
1. 设置用户
```
git config --global user.name "li_yk_oracle_138"  
git config --global user.email "yakun4566@qq.com"
```

## 下载代码运行程序
1. 拉取代码
`git clone git@github.com:yakun4566/network.git`

2. 配置pipenv环境
进入代码目录
`cd network`
生成pipenv目录
`mkdir .venv`

3. 安装pipenv
`pip3 install pipenv`

4. 使用pipenv 安装程序依赖
` pipenv install `

## 自动更新端口并推送到git
`python UpdateUrl.py`



