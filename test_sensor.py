import RPi.GPIO as GPIO
import time

# 定义传感器连接的GPIO引脚
SENSOR_PIN = 23

# GPIO初始化
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)
GPIO.setwarnings(False)

print("--- 红外传感器测试 ---")
print("请用手在传感器上方遮挡和移开，观察状态变化。")
print("按 Ctrl+C 退出。")

try:
    while True:
        # 读取传感器的状态
        sensor_state = GPIO.input(SENSOR_PIN)

        if sensor_state == GPIO.LOW:
            # 通常，检测到物体时（红外光被反射），输出为低电平
            print("状态：检测到物体！(LOW)")
        else:
            # 没有检测到物体时，输出为高电平
            print("状态：空闲 (HIGH)")

        # 每0.5秒打印一次状态
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\n测试结束。")
finally:
    GPIO.cleanup()
