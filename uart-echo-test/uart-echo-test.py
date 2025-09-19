#!/usr/bin/env python3
import serial
import time
import sys
import argparse
import random
def run_echo_server(port, baudrate):
    """
    运行串口echo服务器
    """
    try:
        # 打开串口
        ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1
        )

        print(f"Echo server started on {port} at {baudrate} baud")
        print("Press Ctrl+C to stop the server")

        try:
            while True:
                # 读取数据
                if ser.in_waiting > 0:
                    data = ser.read(ser.in_waiting)
                    print(f"Received: {data.hex()} ({len(data)} bytes)")
                    # 回传数据
                    ser.write(data)
                    print(f"Echoed: {data.hex()} ({len(data)} bytes)")
                time.sleep(0.01)  # 减少CPU占用

        except KeyboardInterrupt:
            print("\nServer stopped by user")

    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
        sys.exit(1)
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Serial port closed")
def run_client(port, baudrate, duration=5, packet_size=16):
    """
    运行串口测试客户端
    """
    try:
        # 打开串口
        ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1
        )

        print(f"Client started on {port} at {baudrate} baud")
        print(f"Testing for {duration} seconds with packet size {packet_size}...")

        start_time = time.time()
        test_count = 0
        success_count = 0
        total_bytes = 0

        try:
            while time.time() - start_time < duration:
                # 生成随机测试数据
                test_data = bytes([random.randint(0, 255) for _ in range(packet_size)])

                # 发送数据
                ser.write(test_data)
                total_bytes += len(test_data)

                # 接收回显
                received = b''
                start_receive = time.time()
                while len(received) < len(test_data) and (time.time() - start_receive) < 2.0:
                    if ser.in_waiting > 0:
                        chunk = ser.read(ser.in_waiting)
                        received += chunk
                    time.sleep(0.001)

                # 验证数据
                if received == test_data:
                    success_count += 1
                    if test_count % 10 == 0:  # 每10次显示一次成功信息
                        print(f"✓ Test {test_count}: Echo correct ({len(test_data)} bytes)")
                else:
                    print(f"✗ Test {test_count}: Echo mismatch!")
                    print(f"  Expected: {test_data.hex()}")
                    print(f"  Received: {received.hex() if received else 'None'}")
                    print(f"  Length: {len(received)} vs {len(test_data)}")

                test_count += 1
                time.sleep(0.1)  # 短暂延迟

        except KeyboardInterrupt:
            print("\nTest stopped by user")

        # 输出测试结果
        elapsed_time = time.time() - start_time
        print(f"\n=== Test Results ===")
        print(f"Total tests: {test_count}")
        print(f"Successful: {success_count}")
        print(f"Total bytes: {total_bytes}")
        print(f"Test duration: {elapsed_time:.2f} seconds")
        print(f"Data rate: {total_bytes/elapsed_time:.2f} bytes/sec" if elapsed_time > 0 else "No data")

        if test_count > 0:
            success_rate = success_count / test_count * 100
            print(f"Success rate: {success_rate:.2f}%")
        else:
            print("No tests performed")

    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
        sys.exit(1)
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Serial port closed")
def main():
    parser = argparse.ArgumentParser(description='Serial Communication Test Tool')

    # 模式选择
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument('-s', '--server', action='store_true',
                           help='Run in server (echo) mode')
    mode_group.add_argument('-c', '--client', action='store_true',
                           help='Run in client (test) mode')

    # 通用参数
    parser.add_argument('port', help='Serial port device (e.g., COM1, /dev/ttyUSB0)')
    parser.add_argument('baudrate', type=int, help='Baud rate (e.g., 9600, 115200)')

    # 客户端专用参数
    parser.add_argument('-d', '--duration', type=int, default=5,
                       help='Test duration in seconds (client mode only, default: 5)')
    parser.add_argument('-p', '--packet-size', type=int, default=16,
                       help='Packet size in bytes (client mode only, default: 16)')

    args = parser.parse_args()

    if args.server:
        run_echo_server(args.port, args.baudrate)
    elif args.client:
        run_client(args.port, args.baudrate, args.duration, args.packet_size)
if __name__ == '__main__':
    main()
