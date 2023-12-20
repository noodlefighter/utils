#!/usr/bin/env python3

# 将子模块推送到镜象站、配置gitmodules等

import os
import shutil
import argparse
import subprocess

MIRROR_SITE_SSH = "ssh://git@example.com/%s.git"
MIRROR_SITE_HTTP = "http://example.com/%s"
ROOTDIR = os.getcwd()

CONFIG_FILE = "submodule-mirrors.txt"
m_dict = {}

def open_dict():
    with open(CONFIG_FILE, 'r') as f:
        for line in f:
            n = 0
            line = line.strip()
            if line:
                n += 1
                s = line.split('|')
                if len(s) < 3:
                    print('ignore line %d, invalid format' % n)
                    continue
                submodule_path = s[0]
                source_url = s[1]
                mirror_name = s[2]
                if len(s) >= 4:
                    submodule_name = s[3]
                else:
                    submodule_name = ''

                submodule_path = submodule_path.strip()
                source_url = source_url.strip()
                mirror_name = mirror_name.strip()
                submodule_name = submodule_name.strip()

                m_dict[submodule_path] = {
                    'source_url': source_url,
                    'mirror_http': MIRROR_SITE_HTTP % mirror_name,
                    'mirror_ssh': MIRROR_SITE_SSH % mirror_name,
                    'mirror_name': mirror_name,
                    'submodule_name': submodule_name
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
    print('DIR %s'%module_dir, 'modules:', modules)

    # 更新子模块的URL为镜象仓库URL
    for m in modules:
        entire_m = os.path.join(module_dir, m)
        print(m, entire_m)
        if entire_m in m_dict:
            mirror_http = m_dict[entire_m]['mirror_http']
            submodule_name = m_dict[entire_m]['submodule_name']
            if submodule_name == '':
                submodule_name = m
            print("set %s -> %s"%(m, mirror_http))
            subprocess.check_call(['git', '-C', module_path, 'config', '-f', '.gitmodules', 'submodule.' + submodule_name + '.url', mirror_http])

    # 拉取
    subprocess.check_call(['git', '-C', module_path, 'submodule', 'update', '--init'])

    # 同步url
    subprocess.check_call(['git', '-C', module_path, 'submodule', 'sync'])

    # 递归遍例每个子模块
    for m in modules:
        submodule_update_recursive(os.path.join(module_dir, m))

def push_mirror():
    for m in m_dict:
        mirror_url = m_dict[m]['mirror_ssh']
        result = subprocess.run(['git', '-C', m, 'push', '--quiet', '--mirror', mirror_url])
        if result.returncode == 0:
            resultStr = 'OK'
        else:
            resultStr = 'FAIL'
        print('%s -> %s: %s'%(m, mirror_url, resultStr))

def push_mirror_bare(submodule):
    subprocess.run(['mkdir', '-p', '.submodule-mirror'])
    with open('.submodule-mirror/.gitignore', 'w') as f:
        f.write('*')

    for m in m_dict:
        # 若指定了submodule，则只处理它
        if not submodule is None:
            if m != submodule:
                continue

        source_url = m_dict[m]['source_url']
        mirror_url = m_dict[m]['mirror_ssh']
        mirror_name = m_dict[m]['mirror_name']
        repo_path = os.path.join('.submodule-mirror', mirror_name)
        if os.path.exists(repo_path):
            shutil.rmtree(repo_path)

        result = subprocess.run(['git', 'clone', '--bare', source_url, repo_path])
        if result.returncode != 0:
            print('clone %s -> %s: FAIL'%(source_url, repo_path))
            continue
        else:
            print('clone %s -> %s: OK'%(source_url, repo_path))


        result = subprocess.run(['git', '-C', repo_path, 'push', '--mirror', mirror_url])
        if result.returncode == 0:
            resultStr = 'OK'
        else:
            resultStr = 'FAIL'
        print('push %s -> %s: %s'%(m, mirror_url, resultStr))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Git Submodule Mirror Tool')
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    show_parser = subparsers.add_parser('show', help='Show command')

    update_submodules_parser = subparsers.add_parser('update-submodules', help='Update submodules command')

    push_parser = subparsers.add_parser('push', help='Push command')
    push_parser.add_argument('submodule', nargs='?', help='submodule name', )

    args = parser.parse_args()

    if args.command == 'update-submodules':
        open_dict()
        submodule_update_recursive('')
    elif args.command == 'show':
        show_submodules()
    elif args.command == 'push':
        open_dict()
        push_mirror_bare(args.submodule)
    else:
        parser.print_help()
