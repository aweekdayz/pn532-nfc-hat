import RPi.GPIO as GPIO
import time

PIN_CLK = 18
PIN_DT = 17
PIN_SW = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_CLK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_DT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_SW, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setwarnings(False)

# --- 用于追踪状态的全局变量 ---
clk_last_state = GPIO.input(PIN_CLK)
counter = 0

def encoder_callback(channel):
    """当CLK或DT引脚状态改变时，都会调用此函数"""
    global clk_last_state, counter

    clk_state = GPIO.input(PIN_CLK)
    dt_state = GPIO.input(PIN_DT)

    if clk_state != clk_last_state:  # 只有在CLK变化时才判断
        if dt_state != clk_state:
            # 顺时针
            counter += 1
            print(f"方向: 顺时针 ->, 计数值: {counter}")
        else:
            # 逆时针
            counter -= 1
            print(f"方向: <- 逆时针, 计数值: {counter}")

    clk_last_state = clk_state

def button_callback(channel):
    print(">> 按钮被按下! <<")

# --- 事件监听 ---
# 现在我们同时监听两个引脚的变化
GPIO.add_event_detect(PIN_CLK, GPIO.BOTH, callback=encoder_callback, bouncetime=1)
GPIO.add_event_detect(PIN_DT, GPIO.BOTH, callback=encoder_callback, bouncetime=1)
GPIO.add_event_detect(PIN_SW, GPIO.FALLING, callback=button_callback, bouncetime=300)

print("--- 旋转编码器宽容模式测试 ---")
print("请旋转或按压旋钮。")
print("按 Ctrl+C 退出。")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n测试结束。")
finally:
    GPIO.cleanup()
