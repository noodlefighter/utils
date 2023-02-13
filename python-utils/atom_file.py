#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

# 模块解决了ubifs下写入关键文件中掉电导致文件数据不完整的问题
# 利用rename在ubifs文件系统下是原子操作的特性
# refer: http://www.linux-mtd.infradead.org/faq/ubifs.html#L_atomic_change

import shutil
import os

class write_open(object):
  def __init__(self, filepath, method):
    self.m_file = filepath
    self.m_tmpfile = os.path.basename(filepath) + '.tmp'
    shutil.copy(self.m_file, self.m_tmpfile)
    self.m_fileobject = open(self.m_tmpfile, method)

  def __enter__(self):
    return self.m_fileobject

  def __exit__(self, type, value, trace):
    os.fsync(self.m_fileobject.fileno())
    self.m_fileobject.close()
    os.rename(self.m_tmpfile, self.m_file)

class tmpfile(object):
  def __init__(self, filepath):
    self.m_file = filepath
    self.m_tmpfile = os.path.basename(filepath) + '.tmp'
    shutil.copy(self.m_file, self.m_tmpfile)

  def __enter__(self):
    return self.m_tmpfile

  def __exit__(self, type, value, trace):
    with open(self.m_tmpfile, 'r') as f:
      os.fsync(f.fileno())
    os.rename(self.m_tmpfile, self.m_file)

#test
# with atom_write_open('abc.txt', 'w') as f:
#   f.write('1234567890')

#test
# with atom_tmpfile('abc.txt') as filename:
#   os.system("echo 'hahahah' > %s" % filename)
