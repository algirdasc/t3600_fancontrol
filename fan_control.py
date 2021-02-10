#!/usr/bin/python3
import configparser
import os
import psutil
import subprocess

APP_PATH = os.path.abspath(os.path.dirname(__file__))
CONFIG_PATH = os.path.join(APP_PATH, 'fans.ini')

config = configparser.ConfigParser()
config.read(CONFIG_PATH)

CPU_TEMP_INPUT = "/sys/class/hwmon/hwmon0/temp1_input"

PWM_CMD="screen -dmS pwm flock -w 1 /tmp/fan_pwm.lck {0}".format(os.path.join(APP_PATH, "pwm.py"))

FAN1 = "/sys/class/hwmon/hwmon0/pwm1"
FAN2 = "/sys/class/hwmon/hwmon0/pwm2"
FAN3 = "/sys/class/hwmon/hwmon0/pwm3"

PWM_IDLE_SPEED = 1
PWM_HOT_SPEED = 128
PWM_CRITICAL_SPEED = 255

def set_pwm_speed(fan, speed):
    speed = str(speed)

    try:
        if config[fan]['speed'] == speed and fan != FAN1 and speed != PWM_CRITICAL_SPEED:
            return
    except Exception:
        pass

    config[fan] = {'speed': speed}

    with open(fan, 'w') as f:
        f.write(speed)

def get_temperature(input):
    with open(input, 'r') as f:
        input = f.readline()
    return float(input) / 1000

# TOP FAN
TEMP_CURRENT = get_temperature(CPU_TEMP_INPUT)
TEMP_HOT = 50
TEMP_CRITICAL = 75

if TEMP_CURRENT >= TEMP_CRITICAL:
   set_pwm_speed(FAN2, PWM_CRITICAL_SPEED)
elif TEMP_CURRENT >= TEMP_HOT and TEMP_CURRENT < TEMP_CRITICAL:
   set_pwm_speed(FAN2, PWM_HOT_SPEED)
else:
   set_pwm_speed(FAN2, PWM_IDLE_SPEED)

# MIDDLE FAN
#TEMP_HOT = 55
#TEMP_CRITICAL = 75

#if TEMP_CURRENT >= TEMP_CRITICAL:
#   set_pwm_speed(FAN3, PWM_CRITICAL_SPEED)
#elif TEMP_CURRENT >= TEMP_HOT and TEMP_CURRENT < TEMP_CRITICAL:
#   set_pwm_speed(FAN3, PWM_HOT_SPEED)
#else:
#   set_pwm_speed(FAN3, PWM_IDLE_SPEED)

# CPU FAN
TEMP_HOT = 69

if TEMP_CURRENT >= TEMP_HOT:
    set_pwm_speed(FAN1, PWM_CRITICAL_SPEED)
else:
    set_pwm_speed(FAN1, PWM_IDLE_SPEED)

with open(CONFIG_PATH, 'w') as f:
    config.write(f)




PWM_FOUND = False
for process in psutil.process_iter():
    cmdline = " ".join(process.cmdline())
    if cmdline.lower() == PWM_CMD.lower():
        PWM_FOUND = True
        break

if PWM_FOUND is False:
    subprocess.run(PWM_CMD.split(" "))
