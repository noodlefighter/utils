#!/usr/bin/env python3

# 将子模块推送到镜象站、配置gitmodules等

import os
import argparse
import subprocess

MIRROR_SITE_SSH = "ssh://git@example.com/%s.git"
MIRROR_SITE_HTTP = "http://example.com/%s"
ROOTDIR = os.getcwd()

CONFIG_FILE = "submodule-mirrors.txt"
m_dict = {}
with open(CONFIG_FILE, 'r') as f:
    for line in f:
        line = line.strip()
        if line:
            submodule_path, source_url, mirror_name = line.split('|')
            submodule_path = submodule_path.strip()
            source_url = source_url.strip()
            mirror_name = mirror_name.strip()

            m_dict[submodule_path] = {
                'source_url': source_url,
                'mirror_http': MIRROR_SITE_HTTP % mirror_name,
                'mirror_ssh': MIRROR_SITE_SSH % mirror_name
            }

# for m in m_dict:
#     print("[%s] %s -> %s" % (m, m_dict[m]['source_url'], m_dict[m]['mirror_http']))

def show_submodules():
    root_dir = os.getcwd()
    result = subprocess.run(['git', 'submodule', 'foreach', '--quiet', '--recursive', 'sh', '-c',
                            'submodule_path=$(pwd); relative_path=$(realpath --relative-to=%s "$submodule_path"); echo "$relative_path|$(git config --get remote.origin.url)"'%root_dir],
                            capture_output=True, text=True)
    if result.returncode == 0:
        output = result.stdout.strip()
        print(output)
    else:
        error = result.stderr.strip()
        print(error)

def get_submodules(path):
    result = subprocess.run(['git', '-C', path, 'submodule', 'status'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print('error!!')
        return []
    output = result.stdout.decode('utf-8').strip()
    arr = []
    if output:
        for line in output.splitlines():
            line = line.strip()
            if line:
                a = line.split(' ')
                if len(a) >= 2:
                    arr.append(a[1])
    return arr

def submodule_update_recursive(module_dir):
    module_path = os.path.join(ROOTDIR, module_dir)
    modules = get_submodules(module_path)
    print('进入 %s'%module_dir, 'modules:', modules)

    # 更新子模块的URL为镜象仓库URL
    for m in modules:
        entire_m = os.path.join(module_dir, m)
        print(m, entire_m)
        if entire_m in m_dict:
            mirror_http = m_dict[entire_m]['mirror_http']
            subprocess.run(['git', '-C', module_path, 'config', '-f', '.gitmodules', 'submodule.' + m + '.url', mirror_http])
            print("set %s -> %s"%(m, mirror_http))

    # 拉取
    subprocess.run(['git', '-C', module_path, 'submodule', 'update', '--init'])

    # 递归遍例每个子模块
    for m in modules:
        submodule_update_recursive(os.path.join(module_dir, m))

# 推送到镜象仓库
def push_mirror():
    for m in m_dict:
        mirror_url = m_dict[m]['mirror_ssh']
        result = subprocess.run(['git', '-C', m, 'push', '--quiet', '--mirror', mirror_url])
        if result.returncode == 0:
            resultStr = 'OK'
        else:
            resultStr = 'FAIL'
        print('%s -> %s: %s'%(m, mirror_url, resultStr))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Git Submodule Mirror Tool')
    parser.add_argument('command', choices=['show', 'update-submodules', 'push'], help='Command to execute')

    args = parser.parse_args()

    if args.command == 'update-submodules':
        submodule_update_recursive('')
    elif args.command == 'show':
        show_submodules()
    elif args.command == 'push':
        push_mirror()
