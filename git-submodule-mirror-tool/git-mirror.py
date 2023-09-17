#!/usr/bin/env python3

# 将子模块推送到镜象站、配置gitmodules等

import os
import argparse
import subprocess

MIRROR_SITE_SSH = "ssh://git@example.com/%s.git"
MIRROR_SITE_HTTP = "http://example.com/%s"
CONFIG_FILE = "submodule-mirrors.txt"

def show_submodules():
    root_dir = os.getcwd()
    result = subprocess.run(['git', 'submodule', 'foreach', '--quiet', '--recursive', 'sh', '-c',
                            f'submodule_path=$(pwd); relative_path=$(realpath --relative-to={root_dir} "$submodule_path"); echo "$relative_path|$(git config --get remote.origin.url)"'],
                            capture_output=True, text=True)
    if result.returncode == 0:
        output = result.stdout.strip()
        print(output)
    else:
        error = result.stderr.strip()
        print(error)

def print_gitmodules(config_file):
    with open(config_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                submodule_path, source_url, mirror_url = line.split('|')

                mirror_url = MIRROR_SITE_HTTP % mirror_url

                submodule_path = submodule_path.strip()
                source_url = source_url.strip()
                mirror_url = mirror_url.strip()

                # 生成.gitmodules内容
                gitmodules_content = f"[submodule \"{submodule_path}\"]\n\tpath = {submodule_path}\n\turl = {mirror_url}\n"

                # 打印.gitmodules内容
                print(gitmodules_content)

def set_gitmodules(config_file):
    with open(config_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                submodule_path, source_url, mirror_url = line.split('|')

                mirror_url = MIRROR_SITE_HTTP % mirror_url

                submodule_path = submodule_path.strip()
                source_url = source_url.strip()
                mirror_url = mirror_url.strip()

                # 更新子模块的URL为镜象仓库URL
                subprocess.run(['git', 'config', '-f', '.gitmodules', 'submodule.' + submodule_path + '.url', mirror_url])

# 推送到镜象仓库
def push_mirror(config_file):
    with open(config_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                submodule_path, source_url, mirror_url = line.split('|')

                submodule_path = submodule_path.strip()
                mirror_url = MIRROR_SITE_SSH % mirror_url

                source_url = source_url.strip()
                mirror_url = mirror_url.strip()

                result = subprocess.run(['git', '-C', submodule_path, 'push', '--quiet', '--mirror', mirror_url])
                if result.returncode == 0:
                    resultStr = 'OK'
                else:
                    resultStr = 'FAIL'
                print('%s -> %s: %s'%(submodule_path, mirror_url, resultStr))



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Git Submodule Mirror Tool')
    parser.add_argument('command', choices=['show', 'get-gitmodules', 'set-gitmodules', 'push'], help='Command to execute')

    args = parser.parse_args()

    if args.command == 'set-gitmodules':
        set_gitmodules(CONFIG_FILE)
    elif args.command == 'get-gitmodules':
        print_gitmodules(CONFIG_FILE)
    elif args.command == 'show':
        show_submodules()
    elif args.command == 'push':
        push_mirror(CONFIG_FILE)
