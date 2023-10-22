# tf卡克隆

磁盘操作，过程完全无提示，谨慎使用，请先了解它行为：

1. 找到所有USB的disk设备
2. 重建GPT格式的分区表，建立一个exFAT分区
3. 将tfcard_files目录的所有文件拷入，执行sync()
4. 卸载磁盘

用法：

```
$ pipenv install
$ pipenv run sudo python3 ./clone-tf.py
```
