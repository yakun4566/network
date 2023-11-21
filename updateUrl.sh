#!/bin/bash

# Mudb文件路径
mudb_file_path="/usr/local/shadowsocksr/mudb.json"
ssr_stop="/etc/init.d/ssrmu stop"
ssr_start="/etc/init.d/ssrmu start"

base_format="{ip}:{port}:{protocol}:{method}:{obfs}:{passwd_base}/?group={group_base}&remarks={remarks_base}"

url_src="url_src.txt"
url_base64="url_base64.txt"
url_2="url_2.txt"

git_commit='git commit -am "提交修改"'
git_push="git push"
git_pull="git pull"

update_mudb_port() {
    mudb_str=$(cat "$mudb_file_path")
    if [ -z "$mudb_str" ]; then
        echo "文件中无内容: $mudb_file_path"
        return 1
    fi

    mudb_json=$(echo "$mudb_str" | jq '.[0]')
    port=$(get_port)
    mudb_json.port=$port
    echo "更新后端口为: $port"
    mudb_str=$(echo "$mudb_str" | jq --argjson mudb_json "$mudb_json" '.[0]=$mudb_json')
    echo "$mudb_str" > "$mudb_file_path"
}

str_to_base64() {
    echo -n "$1" | base64 -w 0 | tr -d '\n='
}

replace_params() {
    ip=$1
    port=$2
    protocol=$3
    method=$4
    obfs=$5
    passwd_base=$(str_to_base64 "$6")
    group_base=$(str_to_base64 "mine")
    remarks_base=$(str_to_base64 "$7")

    echo "$base_format" | \
        sed "s/{ip}/$ip/g" | \
        sed "s/{port}/$port/g" | \
        sed "s/{protocol}/$protocol/g" | \
        sed "s/{method}/$method/g" | \
        sed "s/{obfs}/$obfs/g" | \
        sed "s/{passwd_base}/$passwd_base/g" | \
        sed "s/{group_base}/$group_base/g" | \
        sed "s/{remarks_base}/$remarks_base/g"
}

write_file() {
    echo -n "$2" > "$1"
}

replace_url_src() {
    server=$(echo "$1" | cut -d ':' -f 1)
    lines=$(cat "$url_src")
    index=$(echo "$lines" | grep -n "$server" | cut -d ':' -f 1)
    echo "替换第 $index 行数据"
    if [ -z "$index" ]; then
        lines="$lines$1"
    else
        lines=$(echo "$lines" | sed "${index}s/.*/$1/")
    fi
    write_file "$url_src" "$lines"
}

base64_url() {
    src_lines=$(cat "$url_src")
    base64_list=()

    for line in $src_lines; do
        base64_list+=("ssr://$(str_to_base64 "$line")")
    done

    write_file "$url_base64" "$(echo "${base64_list[*]}" | tr ' ' '\n')"
    write_file "$url_2" "$(str_to_base64 "$(echo "${base64_list[*]}" | tr ' ' '\n')")"
}

get_port() {
    port=$((RANDOM % 64536 + 1000))
    while check_port_in_use "$port"; do
        port=$((RANDOM % 64536 + 1000))
    done
    echo "$port"
}

check_port_in_use() {
    host='127.0.0.1'
    port=$1
    timeout 1 bash -c "</dev/tcp/$host/$port" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "当前端口正在使用: $port"
        return 0
    else
        echo "当前端口未使用: $port"
        return 1
    fi
}

# 主逻辑
git pull
$ssr_stop
update_mudb_port

if [ $? -eq 0 ]; then
    replace_url_src "$(replace_params "${mudb_json[@]}")"
    base64_url

    echo "ssr配置文件更新完成"
    $ssr_start
    $git_commit
    $git_push
else
    echo "ssr配置文件未读取到"
fi
