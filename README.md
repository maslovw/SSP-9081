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

