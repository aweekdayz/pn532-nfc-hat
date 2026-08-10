import RPi.GPIO as GPIO
import time

# --- GPIO 引脚定义 ---
PIN_CLK = 18
PIN_DT = 17
PIN_SW = 27

# --- GPIO 初始化 ---
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_CLK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_DT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_SW, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# 忽略警告信息
GPIO.setwarnings(False)

# --- 回调函数定义 ---
def rotation_callback(channel):
    """当CLK引脚电平变化时调用此函数"""
    time.sleep(0.002) # 增加一个极短的延时来物理防抖
    dt_state = GPIO.input(PIN_DT)
    if dt_state == 0:
        print("方向: 顺时针 ->")
    else:
        print("方向: <- 逆时针")

def button_callback(channel):
    """当SW引脚电平变为低时（被按下）调用此函数"""
    print(">> 按钮被按下! <<")

# --- 添加事件监听 ---
GPIO.add_event_detect(PIN_CLK, GPIO.FALLING, callback=rotation_callback, bouncetime=200)
GPIO.add_event_detect(PIN_SW, GPIO.FALLING, callback=button_callback, bouncetime=300)

# --- 主程序循环 ---
print("--- 旋转编码器测试 ---")
print("请旋转或按压旋钮。")
print("按 Ctrl+C 退出。")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n测试结束。")
finally:
    GPIO.cleanup()
