# 修正二：导入 RPi.GPIO 库，让 GPIO.cleanup() 能正常工作
import RPi.GPIO as GPIO
from pn532 import *
import time

print("正在初始化PN532读卡器...")

try:
    # 使用官方示例中已验证成功的初始化方法
    pn532 = PN532_SPI(debug=False, reset=20, cs=4)
    
    # 修正一：删除多余的 begin() 调用
    # pn532.begin()  <-- 这行是多余的，已删除

    # 获取固件版本以验证通信
    ic, ver, rev, support = pn532.get_firmware_version()
    print(f"成功找到PN532芯片！固件版本: {ver}.{rev}")

    pn532.SAM_configuration()

    print("\n准备就绪，请将一张NFC贴纸放到读卡器上...")
    
    while True:
        uid = pn532.read_passive_target(timeout=0.5)

        if uid is None:
            continue
        
        print("\n读取成功！")
        print("="*40)
        
        uid_hex = ''.join([format(i, '02x') for i in uid])
        
        print(f"这张卡片的UID是: {uid_hex}")
        print("="*40)
        
        break

except Exception as e:
    print(f"发生错误: {e}")
finally:
    # 现在GPIO已经被导入，这行可以正常工作了
    GPIO.cleanup()
