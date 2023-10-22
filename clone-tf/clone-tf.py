import pyudev
import subprocess
import shutil
import re
import hashlib
from colorama import Fore, Style
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# 获取脚本所在路径
import os
script_dir = os.path.split(os.path.realpath(__file__))[0]
os.chdir(script_dir)

source_dirpath = './tfcard_files'
parition_name = "tfcard"

os.system("rm './mylog.txt'")
logfile = os.open('./mylog.txt', os.O_RDWR | os.O_CREAT)

# sysfs例子
# /sys/devices/pci0000:00/0000:00:01.3/0000:01:00.0/usb1/1-6/1-6:1.0/host9/target9:0:0/9:0:0:0/block/sdb
# /sys/devices/pci0000:00/0000:00:08.1/0000:08:00.3/usb3/3-2/3-2.1/3-2.1:1.0/host8/target8:0:0/8:0:0:0/block/sda
# 处理磁盘设备：{'device': '/dev/sdb', 'port': '1-6'}
# 处理磁盘设备：{'device': '/dev/sda', 'port': '3-2.1'}

# 获取USB设备的端口号
# bus-port.port.port:configuration.interface
# 例如2-1.1.3:1.1，其中2-1.1.3是端口号
def get_usb_port(sys_path):
    port_pattern = r'(\d+-\d+(\.\d+)*):\d+\.\d+'
    port_match = re.search(port_pattern, sys_path)
    if port_match:
        port_number = port_match.group(1)
        return port_number
    else:
        return 0

# 更新进度信息
progress_dict = {}
def progress_value_to_text(progress):
    text = ""
    for i in range(0, int(progress/2)): # 100%即50字符宽
        text += ">"
    return text

def update_progress(device, progress, msg = ""):
    global progress_dict
    progress_dict[device["port"]] = {
        "progress": progress,
        "msg": msg
    }

    # print(sorted_devices)

    progress_text = ""

    print("\033c", end="") # 清屏
    for port, val in progress_dict.items():
        if val["progress"] == 0:
            print(Fore.RED, end="")
        elif val["progress"] == 100:
            print(Fore.GREEN, end="")
        else:
            print(Fore.YELLOW, end="")

        print("%08s: %03d%% %s %s" % (port, val["progress"], progress_value_to_text(val["progress"]), val["msg"]))
        print(Style.RESET_ALL, end="")  # 重置颜色



# 创建 exFAT 分区并格式化
def create_exfat_partition(device):

    # 尝试umount，无视结果
    subprocess.run(['umount', '-l', device['node'] + '1', device['node']], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    res = subprocess.run(['parted', '--script', device['node'], 'mklabel', 'gpt'], stdout=subprocess.PIPE, stderr=logfile)
    if res.returncode != 0:
        update_progress(device, 0, "创建分区表失败")
        return False

    res = subprocess.run(['parted', '--script', device['node'], 'mkpart', 'primary', 'ext2', '0%', '100%'], stdout=subprocess.PIPE, stderr=logfile)
    if res.returncode != 0:
        update_progress(device, 0, "创建分区失败")
        return False

    global parition_name
    res = subprocess.run(['mkfs.exfat', '-n', parition_name, device['node']+'1'], stdout=subprocess.PIPE, stderr=logfile)
    if res.returncode != 0:
        update_progress(device, 0, "格式化分区失败")
        return False

    return True

# 挂载分区
def mount_partition(device):

    mount_point = '/mnt/' + device['node'].split('/')[-1]
    res = subprocess.run(['mkdir', '-p', mount_point], stdout=subprocess.PIPE, stderr=logfile)
    if res.returncode != 0:
        update_progress(device, 0, "创建挂载目录失败")
        return None


    res = subprocess.run(['mount', device['node'] + '1', mount_point], stdout=subprocess.PIPE, stderr=logfile)
    if res.returncode != 0:
        update_progress(device, 0, "挂载失败")
        return None

    return mount_point

# 拷贝文件到分区
def copy_files(device, source_dirpath, destination_dirpath):
    for root, dirs, files in os.walk(source_dirpath):
        total_files = len(files)

        i = 0
        for file in files:
            source_filepath = os.path.join(root, file)
            destination_filepath = os.path.join(destination_dirpath, file)
            shutil.copy2(source_filepath, destination_filepath)

            i = i+1
            update_progress(device, 20 + i/total_files*(100-40), "复制文件") # 20-80%

    subprocess.run(['sync', device['node']], stdout=subprocess.PIPE, stderr=logfile)
    subprocess.run(['sync', device['node']], stdout=subprocess.PIPE, stderr=logfile)
    return True

# 卸载分区
def unmount_partition(mount_point):
    subprocess.run(['umount', mount_point], stdout=subprocess.PIPE, stderr=logfile)
    subprocess.run(['rm', '-r', mount_point], stdout=subprocess.PIPE, stderr=logfile)

# 处理单个设备的函数
def process_device(device):
    print(f'处理磁盘设备：{device}')

    # 创建 exFAT 分区
    update_progress(device, 10, "创建分区表")
    if not create_exfat_partition(device):
        return

    # 挂载分区
    update_progress(device, 10, "挂载分区")
    mount_point = mount_partition(device)
    if mount_partition is None:
        return

    # 拷贝文件到分区
    update_progress(device, 20, "复制文件")
    if not copy_files(device, source_dirpath, mount_point):
        return

    # 卸载分区
    update_progress(device, 90, "卸载分区")
    unmount_partition(mount_point)

    update_progress(device, 100, "成功")

    # time.sleep(1)
    # update_progress(device, 20)
    # time.sleep(1)
    # update_progress(device, 50)
    # time.sleep(1)
    # update_progress(device, 100)

def main():

    # 磁盘设备列表
    global devices
    devices = []

    context = pyudev.Context()
    for device in context.list_devices(subsystem='block', DEVTYPE='disk'):
        if 'usb' in device.sys_path:
            # print(device)
            print(device.sys_path)
            print(device.device_node)

            usb_port = get_usb_port(device.sys_path)
            devices.append({
                "node": device.device_node,
                "port": usb_port
            })


    # 清空全局进度
    global progress_dict
    progress_dict.clear()
    for device in devices:
        progress_dict[device["port"]] = {
            "progress": 1,
            "msg": "准备中..."
        }

    # 并行处理每个设备
    with ThreadPoolExecutor() as executor:


        futures = []
        # 提交每个设备的处理任务
        for device in devices:
            future = executor.submit(process_device, device)
            futures.append(future)


        # 监视处理进度
        for future in as_completed(futures):
            # 获取已完成的任务结果
            future.result()

    # 输出运行结果
    cnt_done = 0
    cnt_fail = 0
    for port, val in progress_dict.items():
        if val['progress'] == 0:
            cnt_fail += 1
        elif val['progress'] == 100:
            cnt_done += 1

    print()
    print(Fore.GREEN + "成功:", cnt_done)
    print(Fore.RED + "失败:", cnt_fail)
    print(Style.RESET_ALL, end="")  # 重置颜色


    # 等待用户退出
    while True:
        time.sleep(1)

if __name__ == '__main__':
    main()
