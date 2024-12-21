from gpiozero import Motor
from time import sleep, time

motor = Motor(forward=5, backward=6)
start_time = time()

while True:
    elapsed_time = time() - start_time
    index = int(elapsed_time) % 20 
    
    if index % 10 == 0:
        motor.forward()
    else:
        motor.backward()

    sleep(1)

    if elapsed_time >= 20:
        break

motor.stop()
