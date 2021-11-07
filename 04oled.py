import board
import adafruit_ssd1306
import time
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

"""以下のインストールが必要
$ sudo pip3 install adafruit-circuitpython-ssd1306
$ sudo apt install -y fonts-ipafont
"""

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

# ===========================
OLED_ADDR = 0x3c
FONT_PATH = "/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf"

oled = init_oled(OLED_ADDR)
font = ImageFont.truetype(FONT_PATH, 13)

draw_oled(oled, font, "Hello world!", "こんにちは！")
time.sleep(5)
reset_oled(oled)
