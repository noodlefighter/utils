#!/usr/bin/env python2

# 大部分硬件平台，MAC地址不固定，一般需要写OTP
# 但有时候不想费神搞这些东西，这是个变通的workaround
# 用芯片的UUID通过一定规则，生成固定的MAC地址

import hashlib
import os
import sys

# chip_id_file = '/proc/version' # for test
chip_id_file = '/sys/fsl_otp/HW_OCOTP_CFG1'
chip_id = ''

try:
    with open(chip_id_file, 'r') as f:
        chip_id = f.readline()
except Exception,e:
    print("%s: read chip_id_file(%s) failed(error %d: %s), keep mac addr" % (sys.argv[0], chip_id_file, e.errno, e.strerror))
    exit(1)

h = hashlib.sha256(chip_id).digest()


def get_mac_from_chip_id(id):
    mac = []
    for n in range(6):
        mac.append(ord(h[n]))
    mac[0] = mac[0] & 0xfe  # clear multicast bit
    mac[0] = mac[0] | 0x02  # set local assignment bit (IEEE802)

    mac[5] = mac[5] + id

    for n in range(6):
        mac[n] = "%02x" % mac[n]

    return ':'.join(mac)

def cmd(cmd, check=True):
	ret = os.system(cmd)
	if check and ret != 0:
		raise Exception('Command Exec Error')

def set_mac(interface, mac):
    ret = os.system('ifconfig %s hw ether %s' % (interface, mac))
    if ret != 0:
        print("%s: set %s mac=%s failed..." % (sys.argv[0], interface, mac))
    else:
        print("%s: %s mac=%s" % (sys.argv[0], interface, mac))


eth0_mac = get_mac_from_chip_id(0)
set_mac('eth0', eth0_mac)

eth1_mac = get_mac_from_chip_id(1)
set_mac('eth1', eth1_mac)
