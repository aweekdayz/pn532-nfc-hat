import RPi.GPIO as GPIO
from pn532 import *
import time

# To store the IDs that have already been read in this session
read_ids = set()

print("正在初始化PN532读卡器...")

try:
    # Use the proven, correct initialization for the Waveshare HAT
    pn532 = PN532_SPI(debug=False, reset=20, cs=4)

    # The .begin() method that caused the error has been removed.
    # pn532.begin() # <-- This line was incorrect and is now deleted.

    # Get firmware version to confirm the connection
    ic, ver, rev, support = pn532.get_firmware_version()
    print(f"成功找到PN532芯片！固件版本: {ver}.{rev}")
    
    pn532.SAM_configuration()

    print("\n--- NFC连续读取模式 ---")
    print("可以开始连续刷卡了。")
    print("完成后，请按 Ctrl+C 退出程序。")
    print("="*40)

    while True:
        uid = pn532.read_passive_target(timeout=0.5)

        if uid is None:
            continue
        
        uid_hex = ''.join([format(i, '02x') for i in uid])
        
        if uid_hex in read_ids:
            print(f"提示：ID {uid_hex} 已经登记过了。")
        else:
            read_ids.add(uid_hex)
            print(f"\n读取成功！新ID: {uid_hex}")
            print("请记录下这个ID，然后可以放上下一张卡。")
        
        # Wait 3 seconds to give you time to remove the card
        time.sleep(3)

except KeyboardInterrupt:
    print("\n\n程序已退出。本次运行登记的ID列表：")
    if read_ids:
        for i, uid in enumerate(read_ids):
            print(f"{i+1}: {uid}")
    else:
        print("未登记任何新ID。")
    
except Exception as e:
    print(f"\n发生错误: {e}")
finally:
    GPIO.cleanup()