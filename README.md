# SSP-9081
Python control over Manson SSP-9081 Power Source 

![SSP-9081_FrontPanel](https://github.com/maslovw/SSP-9081/blob/master/doc/front_panel.png)

# Installation
`pip install .`

# Usage
## Serial interface

```python
import ssp_9081
from ssp_9081.interfaces import SSP_9081_Serial
from ssp_9081 import SSP_9081

com = SSP_9081_Serial('COM3')
power = SSP_9081(com)

power.setU(12.) # set voltage 12V
power.setOut(True) # turn it on

print(power.getUI())
print(power.getPower())
```

## command line
```bash
ssp9081 --help
usage: ssp9081 [-h] [-p PORT] [-u SETU] [-i SETI] [-on] [-off] [--getU]
               [--getI] [--getOut] [--hwversion]

Script to control SSP_9081 via serial(USB) interfacessp9081 --off -u=12 --on:
will turnoff the output, set 12V and turn the power on

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Serial port name, default is taken from ENV_VAR
                        "SSP_9081"
  -u SETU, --setU SETU  Set Voltage (float value)
  -i SETI, --setI SETI  Set Current (float value)
  -on, --on             set to turn on the power, last action to execute
  -off, --off           set to turn off the power, first action to execute if
                        specified
  --getU                print Voltage
  --getI                print Current
  --getOut              print if the power is on or off
  --hwversion           print version returned by SSP_9081
```

Example: 
```bash
>> ssp9081 --setU=12 --on
setU(12.0V):  True
setOn:  True

>> ssp9081 --off --setU=6.5 --setI=2 --on
setOff:  True
setI(2.0A):  True
setU(6.5V):  True
setOn:  True

>> ssp9081 --getU
getU:  6.51

>> ssp9081 --getI
getI:  1.456

>> ssp9081 --hwversion
Version:  Rev1.2
```
