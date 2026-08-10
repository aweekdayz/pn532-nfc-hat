import RPi.GPIO as GPIO
import time

# 定义GPIO引脚
# 使用 BCM 编号方式
CLK_PIN = 17
DT_PIN = 27
SW_PIN = 22

# 全局变量
counter = 0
last_clk_state = 0
clk_state = 0
dt_state = 0
last_button_state = GPIO.HIGH

def setup():
    """初始化设置"""
    GPIO.setmode(GPIO.BCM)
    # 设置CLK, DT, SW为输入引脚，并启用上拉电阻
    # 上拉电阻确保在没有信号时，引脚保持高电平
    GPIO.setup(CLK_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(DT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(SW_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    # 捕获CLK引脚的下降沿事件，并设置200ms的防抖动
    GPIO.add_event_detect(CLK_PIN, GPIO.FALLING, callback=rotary_callback, bouncetime=200)
    # 捕获SW引脚的下降沿事件，并设置300ms的防抖动
    GPIO.add_event_detect(SW_PIN, GPIO.FALLING, callback=switch_callback, bouncetime=300)
    
    print("KY-040 测试已启动。请旋转或按下旋钮。")
    print("按下 Ctrl+C 退出。")

def rotary_callback(channel):
    """旋转编码器回调函数"""
    global counter
    
    # 读取CLK和DT的当前状态
    clk_state = GPIO.input(CLK_PIN)
    dt_state = GPIO.input(DT_PIN)
    
    # CLK引脚触发了下降沿，所以我们检查DT引脚的状态来判断方向
    # 这是标准的正交编码器解码逻辑
    if dt_state == GPIO.LOW:
        counter += 1
        print(f"方向: 顺时针 -> 计数: {counter}")
    else:
        counter -= 1
        print(f"方向: 逆时针 -> 计数: {counter}")

def switch_callback(channel):
    """开关回调函数"""
    print("开关被按下!")

def main():
    """主函数循环"""
    try:
        while True:
            # 主循环可以保持空闲，因为所有工作都由中断处理
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("程序退出。")
    finally:
        # 清理GPIO设置
        GPIO.cleanup()

if __name__ == '__main__':
    setup()
    main()
