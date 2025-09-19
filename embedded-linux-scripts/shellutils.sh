
# 输入若干个字符串参数，将这些字符串连接起来，逐字符的ASCII编码值相加，返回校验和
calc_strings_checksum() {
    checksum=0

    for arg in "$@"; do
        length=${#arg}
        for ((i=0; i<$length; i++)); do
            char=${arg:$i:1}
            ascii=$(printf "%d" "'$char")
            checksum=$((checksum + ascii))
        done
    done

    echo $checksum
}

# 遍历指定的文件夹，执行每一个文件，如果返回值非0，则立即返回这个非0的返回值
execute_files() {
    local folder="$1"
    local return_value=0

    # 遍历指定的文件夹
    for file in "$folder"/*; do
        # 检查文件是否可执行
        if [[ -x "$file" ]]; then
            # 执行文件
            "$file"
            local result=$?
            # 如果返回值非0，则立即返回
            if [[ $result -ne 0 ]]; then
                return_value=$result
                break
            fi
        fi
    done

    return $return_value
}
