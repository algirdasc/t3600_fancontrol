# t3600_fancontrol
Dell Precision T3600 dirty PWM fancontrol

Well it is not real PWM, rather dirty implementation to achieve optimal-ish cooling, somewhere between quiet & hot and full speed jet engine sound barrier.

# Why?
I'am running T3600 with Intel(R) Xeon(R) CPU E5-2665 (8 core) as my home lab / server. To gain [WAF](https://en.wikipedia.org/wiki/Wife_acceptance_factor), I had to quiet it down. Since BIOS does crappy job keeping machine cool / quiet, I had to improvise.

# Installation
Run it periodically, just put this in your cron, and it should do the rest. You might need to install `python-psutil` package using `pip` or your OS package manager.

# How it works?
I've noticed that CPU fan has two states - full speed and idle speed, nothing in between. I've managed to calculate pseudo-PWM value which is related to CPU & ambient temp, so it now regulates fan speed between idle/full constantly, allowing fan to spin at middle speeds. This pseudo-PWM works only when CPU temp is between LOW_LIMIT and HIGH_LIMIT. Feel free to change it to your needs in `pwm.py`.

T3600 has three front fans - top and middle can be controlled by PWM, third spins at constant speed, we won't talk about this one. Other two can be controlled between idle speed (~800 RPM), low speed (~1200 RPM) and high speed (~4000+ RPM).

`fan_control.py` logic is to increase front fans first when CPU temp rises, if that won't help, `pwm.py` which controls CPU fan speed should do the job and if CPU still getting hot, full speed mode should activate when temperature reaches ~70 C.

My temperatures and RPM at idle:

```
load average: 3,38, 3,37, 3,62

Processor Fan: 1611 RPM
Other Fan:      766 RPM
Other Fan:     2000 RPM
CPU:            +46.0°C  
Ambient:        +21.0°C
```

P.S: I've commented out middle fan (PWM3). I've left medium fan speed in BIOS and this setting keeps middle fan at ~2k RPM constantly without much noise.
