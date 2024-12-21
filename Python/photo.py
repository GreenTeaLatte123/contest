from gpiozero import DigitalInputDevice
from time import sleep

# GPIO 핀 4번을 입력 장치로 설정합니다.
input_device = DigitalInputDevice(4)

# 5번의 반복 동안 입력 값을 읽어와서 출력합니다.
for i in range(5):
    print(input_device.value)
    sleep(1)  # 1초 대기
