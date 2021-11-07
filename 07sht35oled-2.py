import smbus
import time
from datetime import datetime

import board
import adafruit_ssd1306
import time
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

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
    return(dt.strftime("%m/%d"))

def ptime(dt):
    """時刻表示フォーマット
    """
    return(dt.strftime("%H:%M:%S"))

def reset_oled(oled):
    """ディスプレイの表示リセット
    """
    oled.fill(0)
    oled.show()

def init_oled(addr):
    """ディスプレイ使用準備
    """
    i2c = board.I2C()
    oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=addr)
    reset_oled(oled)
    return(oled)

def draw_oled(oled, font, line1, line2):
    """ディスプレイにテキストを表示
    """
    image = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), line1, font=font, fill=255)
    draw.text((0, 20), line2, font=font, fill=255)
    oled.image(image)
    oled.show()

def measure(addr, bus):
    """温湿度と計測時刻を取得する
    """
    now = datetime.now()
    data = get_data(addr, bus)
    t = temp(data) 
    h = humi(data) 
    return(now, t, h)

def output(oled, now,t, h):
    """計測結果を出力する
    """
    print(f'{pdate(now)} {ptime(now)}, {t:.2f}℃, {h:.2f}%')
    draw_oled(oled, font, 
        f'{pdate(now)} {ptime(now)}', 
        f'{t:.2f}℃, {h:.2f}%')

# ===========================
SHT35_ADDR = 0x44
OLED_ADDR = 0x3c
FONT_PATH = "/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf"

oled = init_oled(OLED_ADDR)
font = ImageFont.truetype(FONT_PATH, 14)
bus = init_sht35(SHT35_ADDR)
try:
    while True:
        now, t, h = measure(SHT35_ADDR, bus)
        output(oled, now, t, h)
        time.sleep(1)
finally:
    reset_oled(oled)
