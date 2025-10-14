#!/bin/bash
# 用法: ./run_py.sh tools/amap_city_code.py

if [ $# -lt 1 ]; then
    echo "请指定要运行的 Python 文件"
    exit 1
fi

PY_FILE="$1"

# 获取项目根目录（当前脚本上两层目录）
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

# 把根目录加入 PYTHONPATH
export PYTHONPATH=".:$PYTHONPATH"

# 运行 Python 文件
python3 "./$PY_FILE"