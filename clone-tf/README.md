# tf卡克隆

磁盘操作，过程完全无提示，谨慎使用，请先了解它行为：

1. 找到所有USB的disk设备
2. 重建GPT格式的分区表，建立一个exFAT分区
3. 将tfcard_files目录的所有文件拷入，执行sync()
4. 卸载磁盘

用法：

1. 配置代码中的usbdevice_vid_pid为实际使用的USB读卡器的vid和pid

2. （可选）如果需要免sudo命令，则需要为当前用户配置权限，默认能操作磁盘的group为`disk`，如：

```
$ ls /dev/sda -lah
brw-rw---- 1 root disk 8, 0 10月22日 15:50 /dev/sda
```

所以要将当前用户添加进disk组，logout后重新登入：

```
$ sudo gpasswd -a $USER disk
```

3. 运行程序，日志请查看目录下的mylog.txt

```
$ pipenv install
$ pipenv run python ./clone-tf.py
```
