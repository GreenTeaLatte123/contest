# stepmotor.py

import threading
from gpiozero import OutputDevice
from time import sleep

StepPins = [12, 16, 20, 21]

# 핀 출력 설정
step_pins = [OutputDevice(pin) for pin in StepPins]

# 싱글 코일 움직임 방식 시퀀스
StepCount = 4

Seq1 = [[0, 0, 0, 1],
        [0, 0, 1, 0],
        [0, 1, 0, 0],
        [1, 0, 0, 0]]

Seq2 = [[1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]]

StepCounter = threading.local()  # 스레드 별로 독립적인 StepCounter 초기화

def left():
    global StepCounter
    StepCounter.value = 0  # 각 스레드별로 독립적인 StepCounter 초기화
    try:
        total_steps = 400 * StepCount  # 총 스텝 수 (4바퀴)
        current_step = 0

        while current_step < total_steps:  # 총 스텝 수까지 반복
            for pin in range(4):
                xpin = step_pins[pin]
                xpin.value = bool(Seq1[StepCounter.value][pin])

            StepCounter.value += 1  # 1 증가

            # 시퀀스가 끝나면 다시 시작
            if StepCounter.value == StepCount:
                StepCounter.value = 0
            if StepCounter.value < 0:
                StepCounter.value = StepCount

            # 다음 동작 기다리기
            sleep(0.005)
            current_step += 1

    except KeyboardInterrupt:
        for pin in step_pins:
            pin.close()

def right():
    global StepCounter
    StepCounter.value = 0  # 각 스레드별로 독립적인 StepCounter 초기화
    try:
        total_steps = 400 * StepCount  # 총 스텝 수 (4바퀴)
        current_step = 0

        while current_step < total_steps:  # 총 스텝 수까지 반복
            for pin in range(4):
                xpin = step_pins[pin]
                xpin.value = bool(Seq2[StepCounter.value][pin])

            StepCounter.value += 1  # 1 증가

            # 시퀀스가 끝나면 다시 시작
            if StepCounter.value == StepCount:
                StepCounter.value = 0
            if StepCounter.value < 0:
                StepCounter.value = StepCount

            # 다음 동작 기다리기
            sleep(0.005)
            current_step += 1

    except KeyboardInterrupt:
        for pin in step_pins:
            pin.close()
