# utils_pump.py
# 同济子豪兄 2024-5-22
# GPIO引脚、吸泵相关函数

print('导入夹爪模块')
import sys
import serial
import time

try :
        com = serial.Serial(
        port = 'COM3',
        baudrate = 115200,
        bytesize = serial.EIGHTBITS,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE)

except Exception as e:
        print(f"串口连接异常：{e}")
    
print(f"串口连接完成")

def pump_on():
    '''
    夹
    '''
    print('夹')
    com.close()
    com.open()
    hex_str = '01109C400001020000F499'
    com.write(bytes.fromhex(hex_str))

def pump_off():
    '''
    放
    '''
    print('放')
    com.close()
    com.open()
    hex_str = '01109C400001020064F572'
    com.write(bytes.fromhex(hex_str))
    