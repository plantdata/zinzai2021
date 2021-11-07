import smbus
import time
from datetime import datetime

def init_sht35(addr):
    """sht35の使用準備
    """
    bus = smbus.SMBus(1)
    bus.write_byte_data(addr, 0x21, 0x30)
    time.sleep(1)
    return(bus)

def get_data(addr, bus):
    """計測データの取得
    """
    bus.write_byte_data(addr, 0xE0, 0x00)
    data = bus.read_i2c_block_data(addr, 0x00, 6)
    return(data)

def bin2int(msb, lsb):
    """バイト列を整数に変換する
    """
    return(int.from_bytes([msb, lsb], byteorder='big', signed=False))

def temp(data):
    """測定値を摂氏に変換
    """
    v = bin2int(data[0], data[1])
    t = -45 + 175 * (v / (2**16 - 1))
    return(t)

def humi(data):
    """測定値を相対湿度に変換
    """
    v = bin2int(data[3], data[4])
    h = 100 * (v / (2**16 - 1))
    return(h)

def pdate(dt):
    """日時表示フォーマット
    """
    return(dt.strftime("%Y-%m-%d"))

def ptime(dt):
    """時刻表示フォーマット
    """
    return(dt.strftime("%H:%M:%S"))

# ===========================
I2C_ADDR = 0x44
bus = init_sht35(I2C_ADDR)

while True:
    now = datetime.now()
    data = get_data(I2C_ADDR, bus)
    t = temp(data) 
    h = humi(data) 

    print(f'{pdate(now)} {ptime(now)}, {t:.2f}℃, {h:.2f}%')
    time.sleep(1)
