#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import sys
import yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


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


def __load_file(name):
    with open(name) as f:
        return yaml.load(f, Loader=Loader)

def merge_files(files):
    files = [__load_file(name) for name in file_names]
    result = {}
    for data in files:
        result = __merge(result, data)
    return result # return yaml node

def merge_files_and_dump_file(files, dump_file):
    yaml_node = merge_files(files)
    with open(dump_file, 'w') as f:
        f.write(yaml.dump(merge_files(file_names), allow_unicode=True))

# CLI
if __name__ == '__main__':
    file_names = sys.argv[1:]
    # merge_files_and_dump_file(file_names, 'test.yaml')
    print(yaml.dump(merge_files(file_names), Dumper=Dumper, allow_unicode=True))
