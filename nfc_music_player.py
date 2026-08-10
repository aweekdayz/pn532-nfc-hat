import os
import time
import RPi.GPIO as GPIO
from pn532 import *

# --- 核心配置区 ---
# 在这里，填入你刚刚用 get_id.py 登记好的真实ID和专辑信息
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
    # ↑↑↑ 请用你的真实ID（十六进制字符串）和元数据替换这里的示例 ↑↑↑
}

print("正在初始化PN532读卡器...")

try:
    # --- 使用已验证成功的初始化方法 ---
    pn532 = PN532_SPI(debug=False, reset=20, cs=4)
    pn532.SAM_configuration()
    # --------------------------------

    print("唱片机服务已启动，等待NFC唱片...")

    while True:
        uid = pn532.read_passive_target(timeout=0.5)

        if uid is None:
            continue

        uid_hex = ''.join([format(i, '02x') for i in uid])

        print(f"\n检测到唱片，ID: {uid_hex}")

        if uid_hex in ALBUM_MAP:
            album_info = ALBUM_MAP[uid_hex]
            artist = album_info['artist']
            album = album_info['album']

            print(f"匹配成功！正在加载专辑: {artist} - {album}")

            # --- 正确的MPC命令顺序 ---
            # 1. 停止并清空播放列表
            os.system("mpc -h localhost stop")
            os.system("mpc -h localhost clear")
            # 2. 加载新的专辑歌曲
            command = f"mpc -h localhost findadd artist \"{artist}\" album \"{album}\""
            os.system(command)
            # 3. 在播放之前，预设好音量！
            os.system("amixer sset 'Master' 24%")
            # 4. 最后，开始播放
            os.system("mpc -h localhost play")
            print(f"专辑《{album}》已开始播放。")
        else:
            print("未知的唱片ID，资料库中无此专辑。")

        time.sleep(3)

except Exception as e:
    print(f"发生错误: {e}")
finally:
    GPIO.cleanup()
