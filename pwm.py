#!/usr/bin/python3
import time

LOW_LIMIT=40
HIGH_LIMIT=70
ON = 255
OFF = 1
FAN = "/sys/class/hwmon/hwmon0/pwm1"
CPU_TEMP_INPUT = "/sys/class/hwmon/hwmon0/temp1_input"
AMBIENT_TEMP_INPUT = "/sys/class/hwmon/hwmon0/temp3_input"

def get_temperature(path):
    with open(path, 'r') as f:
        temperature = f.readline()
    return int(temperature) / 1000

def get_cpu_temp():
    return get_temperature(CPU_TEMP_INPUT)

def get_ambient_temp():
    return get_temperature(AMBIENT_TEMP_INPUT)

def set_state(state):
    with open(FAN, 'w') as f:
        f.write(str(state))

i = 0
state = ON
while True:
    i += 1

    cpu_temp = get_cpu_temp()
    if cpu_temp < LOW_LIMIT or cpu_temp >= 72:
        print("cpu is not in pwm temperature, t={0}".format(cpu_temp))
        if cpu_temp < LOW_LIMIT:
            set_state(OFF)
        else:
            set_state(ON)
        time.sleep(10)
        continue

    state = ON if state == OFF else OFF

    ambient_temp = get_ambient_temp()
    sleep = ambient_temp / 10 / 2
    sleep = sleep + (cpu_temp - ambient_temp) / 100
    sleep = sleep - (0.5 if state == ON else 0) # spin down takes longer than spin up
    print("sleep is {0}, state is {1}".format(sleep, state))

    if i == 30:
        print("recalibrating fan rpm")
        set_state(OFF)
        sleep = 5
        i = 0
    else:
        set_state(state)

    time.sleep(sleep)

