# SSP-9081
Python control over Manson SSP-9081 Power Source 

# Usage
## Serial interface

import ssp_9081
from ssp_9081.ssp_9081_interfaces import SSP_9081_Serial
from ssp_9081 import SSP_9081

com = SSP_9081_Serial('COM1')
power = SSP_9081(com)

power.setU(12.) # set voltage 12V
power.setOut(True) # turn it on
