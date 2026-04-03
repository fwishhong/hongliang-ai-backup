#!/bin/bash
# DeepReader wrapper - 自动加载代理配置
cd ~/OpenClaw-DeepReeder
source .venv/bin/activate

# 加载代理配置
export HTTP_PROXY=http://127.0.0.1:7897
export HTTPS_PROXY=http://127.0.0.1:7897
export NO_PROXY=localhost,127.0.0.1

# 运行 DeepReader
python3 -c "
import os
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7897'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7897'

from deepreader_skill import run
import sys
url = sys.argv[1] if len(sys.argv) > 1 else ''
if url:
    result = run(url)
    print(result)
else:
    print('Usage: deepreader \"<URL>\"')
"
