import os
import time
import RPi.GPIO as GPIO
from pn532 import *

# --- GPIO 引脚定义 ---
PIN_ENCODER_CLK = 18
PIN_ENCODER_DT = 17
PIN_ENCODER_SW = 27
PIN_IR_SENSOR = 23
volume_step = 5

# --- NFC 核心配置 ---
ALBUM_MAP = {
    '1df5f2e9111080': {"artist": "Billie Eilish", "album": "HIT ME HARD AND SOFT"},
    '1df2f2e9111080': {"artist": "The Weeknd", "album": "Hurry Up Tomorrow"},
    '1df4f2e9111080': {"artist": "The Weeknd", "album": "After Hours"},
    '1df3f2e9111080': {"artist": "Justin Bieber", "album": "Changes"},
    '1df6f2e9111080': {"artist": "The Weeknd", "album": "Dawn FM [Alternate World]"},
    '1df7f2e9111080': {"artist": "Playboi Carti", "album": "Die Lit"},
    '1df8f2e9111080': {"artist": "Calvin Harris", "album": "Funk Wav Bounces, Vol.1"},
    '1df9f2e9111080': {"artist": "Dua Lipa", "album": "Future Nostalgia [The Moonlight Edition]"},
    '1dfdf2e9111080': {"artist": "Kendrick Lamar", "album": "good kid, m.A.A.d city (deluxe)"},
    '1dfcf2e9111080': {"artist": "Billie Eilish", "album": "Happier Than Ever"},
    '1dfbf2e9111080': {"artist": "Don Toliver", "album": "HARDSTONE PSYCHO"},
    '1dfaf2e9111080': {"artist": "Future", "album": "HNDRXX"},
}

# --- GPIO 初始化 ---
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_ENCODER_CLK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_ENCODER_DT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_ENCODER_SW, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_IR_SENSOR, GPIO.IN)
GPIO.setwarnings(False)

# --- 初始化 PN532 ---
try:
    pn532 = PN532_SPI(debug=False, reset=20, cs=4)
    time.sleep(0.5)
    ic, ver, rev, support = pn532.get_firmware_version()
    print(f"成功找到 PN532 v{ver}.{rev}")
    pn532.SAM_configuration()
except Exception as e:
    print(f"PN532 初始化失败: {e}")
    GPIO.cleanup()
    exit()

# --- 主程序 ---
if __name__ == '__main__':
    # 状态变量初始化
    SYSTEM_STATE = 'IDLE' 
    last_uid_hex = None
    clk_last_state = GPIO.input(PIN_ENCODER_CLK)
    sw_last_state = GPIO.input(PIN_ENCODER_SW)
    
    print("最终版唱片机已启动（轮询模式），所有功能就绪。")
    try:
        # --- 统一主循环 ---
        while True:
            # -- 轮询编码器旋转 (使用你验证过的最终版逻辑) --
            clk_state = GPIO.input(PIN_ENCODER_CLK)
            if clk_state != clk_last_state:  # 只在CLK引脚状态变化时才判断
                dt_state = GPIO.input(PIN_ENCODER_DT)
                # 使用你测试成功的最准确的判断逻辑
                if dt_state != clk_state:
                    os.system(f"amixer sset 'Master' {volume_step}%+") # 顺时针
                else:
                    os.system(f"amixer sset 'Master' {volume_step}%-") # 逆时针
            clk_last_state = clk_state

            # -- 轮询编码器按压 --
            sw_state = GPIO.input(PIN_ENCODER_SW)
            if sw_state == GPIO.LOW and sw_last_state == GPIO.HIGH: # 检测到按下的瞬间
                print("按钮按下 -> 播放/暂停")
                os.system("mpc toggle")
            sw_last_state = sw_state

            # -- 状态机逻辑（唱臂和NFC） --
            tonearm_is_lifted = (GPIO.input(PIN_IR_SENSOR) == GPIO.HIGH)

            if SYSTEM_STATE == 'IDLE' and tonearm_is_lifted:
                print("唱臂已拿起，进入扫描模式...")
                SYSTEM_STATE = 'SCANNING'
            
            elif SYSTEM_STATE == 'SCANNING':
                if not tonearm_is_lifted:
                    print("扫描中途唱臂归位，返回待机。")
                    SYSTEM_STATE = 'IDLE'
                    continue

                uid = pn532.read_passive_target(timeout=0.2)
                if uid is not None:
                    uid_hex = ''.join([format(i, '02x') for i in uid])
                    if uid_hex != last_uid_hex:
                        last_uid_hex = uid_hex
                        print(f"扫描到唱片 ID: {uid_hex}")
                        if uid_hex in ALBUM_MAP:
                            album_info = ALBUM_MAP[uid_hex]
                            print(f"匹配成功！正在加载专辑: {album_info['artist']} - {album_info['album']}")
                            os.system("mpc clear")
                            os.system(f"mpc findadd artist \"{album_info['artist']}\" album \"{album_info['album']}\"")
                            os.system("amixer sset 'Master' 24%")
                            os.system("mpc play")
                            SYSTEM_STATE = 'PLAYING'
                        else:
                            print("未知的唱片ID。")
                            SYSTEM_STATE = 'PLAYING' 
            
            elif SYSTEM_STATE == 'PLAYING' and not tonearm_is_lifted:
                print("唱臂已归位，停止播放...")
                os.system("mpc stop")
                last_uid_hex = None
                SYSTEM_STATE = 'IDLE'

            time.sleep(0.01) # 主循环延时，降低CPU占用

    except KeyboardInterrupt:
        print("\n程序已停止。")
    finally:
        GPIO.cleanup()