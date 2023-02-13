# -*- coding: UTF-8 -*-

import sys
import yaml  # pyyaml == 3.11

try:
    from yaml import SafeLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

# dump成yml文本
def dump(yaml_obj):
    if yaml_obj is None:
        return ""
    elif isinstance(yaml_obj, dict):
        return yaml.dump(yaml_obj, allow_unicode=True, default_flow_style=False)
    else:
        return str(yaml_obj)

def load_file(file):
    with open(file) as f:
        data = yaml.load(f, Loader=Loader)
        if isinstance(data, dict):
            return data
        else:
            return None

def save_file(yaml_obj, file):
    with open(file, 'w') as f:
        f.write(dump(yaml_obj))


def get(yaml_obj, path, default=None):
    paths = path.split('/')
    try:
        for i in paths:
            yaml_obj = yaml_obj[i]
    except KeyError:
        return default
    return yaml_obj

def set(yaml_obj, path, value):
    def loop_set(obj, paths):
        new = {}
        path_found = False
        for k in obj.keys():
            if k == paths[0]:
                path_found = True
                if len(paths) == 1:
                    new[k] = value
                else:
                    new[k] = loop_set(obj.get(k, {}), paths[1:])
            else:
                new[k] = obj[k]

        if not path_found:
            raise KeyError
        return new

    paths = path.split('/')
    try:
        new_conf = loop_set(yaml_obj, paths)
    except KeyError:
        return None

    return new_conf

# Mutating recursive dictionary merge
def __merge(a, b):
    if isinstance(a, dict) and isinstance(b, dict):
        for k, v in b.items():
            if k in a:
                a[k] = __merge(a[k], v)
            else:
                a[k] = v
        return a
    else:
        return b

def merge_files(files):
    files = [load_file(name) for name in files]
    result = {}
    for data in files:
        if data is None:
            data = {}
        result = __merge(result, data)
    return result # return yaml node

def merge_files_and_dump_file(files, dump_file):
    save_file(merge_files(files), dump_file)

# b中除去于a相同的项
def __diff(a, b):
    if isinstance(a, dict) and isinstance(b, dict):
        new_b = {}
        for k, v in b.items():
            if k in a:
                res = __diff(a[k], v)
                if res != None:
                    new_b[k] = res
            else:
                new_b[k] = v
        if new_b == {}:
            return None
        else:
            return new_b

    elif not isinstance(a, dict) and not isinstance(b, dict):
        if a == b:
            return None
        else:
            return b
    else:
        return b

def __test_diff():
    # 修改项
    a = {'x': {'y1':1, 'y2':2}}
    b = {'x': {'y1':1, 'y2':3}}
    answer = {'x': {'y2':3}}
    print("test1 %s" % ("OK" if (__diff(a, b) == answer) else "FAIL"))
    # 添加项
    a = {'x': {'y1':1, 'y2':2}}
    b = {'x': {'y1':1, 'y2':2, 'y3': 4}}
    answer = {'x': {'y3':4}}
    print("test2 %s" % ("OK" if (__diff(a, b) == answer) else "FAIL"))
    # 项类型改变
    a = {'x': {'y1':1, 'y2':2}}
    b = {'x': {'y1':"haha", 'y2':{'z': 123}}}
    answer = {'x': {'y1': "haha", 'y2':{'z':123}}}
    print("test3 %s" % ("OK" if (__diff(a, b) == answer) else "FAIL"))
    # 项减少
    a = {'x': {'y1':1, 'y2':2}}
    b = {'x': {'y2':2}}
    answer = None
    print("test4 %s" % ("OK" if (__diff(a, b) == answer) else "FAIL"))
    # 错误输入
    a = {'x': {'y1':1, 'y2':2}}
    b = None
    answer = None
    print("test5 %s" % ("OK" if (__diff(a, b) == answer) else "FAIL"))
    # 错误输入
    a = None
    b = {'x': {'y1':1, 'y2':2}}
    answer = {'x': {'y1':1, 'y2':2}}
    print("test6 %s" % ("OK" if (__diff(a, b) == answer) else "FAIL"))

# 找出file与叠加后的files的不同之处
def diff_with_files(file, files):
    files_data = [load_file(name) for name in files]
    a = {}
    for data in files_data:
        if data is not None:
            a = __merge(a, data)

    b = load_file(file)
    if b is None:
        b = {}
    result = __diff(a, b)
    return result # return yaml node

def diff_with_files_and_dump_file(file, files, dump_file):
    data = diff_with_files(file, files)
    if data is None:
        data = {}
    save_file(data, dump_file)

# CLI
if __name__ == '__main__':
    # __test_diff()

    cmd = sys.argv[1]
    file_names = sys.argv[2:]

    if cmd == "diff":
        print(dump(diff_with_files(file_names[0], file_names[1:])))
    elif cmd == "merge":
        # merge_files_and_dump_file(file_names, 'test.yaml')
        print(dump(merge_files(file_names)))
    else:
        print("usage:")
        print(" %s diff <compared_file> <files ...>" % sys.argv[0])
        print(" %s merge <files ...>" % sys.argv[0])
