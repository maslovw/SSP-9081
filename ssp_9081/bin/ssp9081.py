#!python3
__version__ = "1.0.13"

# import ssp_9081
import argparse
import time
import os

from ssp_9081.interfaces import SSP_9081_Serial
from ssp_9081 import SSP_9081

RET_OK = 0
RET_TIMEOUT = 1
RET_WRONG_SETTINGS = 2

def main():
    ret_code = RET_OK

    env_port = os.environ.get('SSP_9081', None)
    parser = argparse.ArgumentParser(description='Script to control SSP_9081 via serial(USB) interface'
                                                 'ssp9081 --off -u=12 --on:  will turnoff the output, set 12V and turn the '
                                                 'power on')

    parser.add_argument('-p', '--port',
                        default=env_port,
                        help='Serial port name, default is taken from ENV_VAR "SSP_9081"')
    parser.add_argument('-u', '--setU',
                        type=float,
                        default=None,
                        help='Set Voltage (float value)')
    parser.add_argument('-i', '--setI',
                        type=float,
                        default=None,
                        help='Set Current (float value)')
    parser.add_argument('-on', '--on',
                        action='store_true',
                        help='set to turn on the power, last action to execute')
    parser.add_argument('-off', '--off',
                        action='store_true',
                        help='set to turn off the power, first action to execute if specified')
    parser.add_argument('--waitU',
                        default=None,
                        type=float,
                        help='wait for the setU action to be applied with timeout, --waitU=0 to wait without timeout')
    parser.add_argument('--setWaveForm',
                        type=str,
                        default=None,
                        help='waveform csv file: (step,voltage,time)')
    parser.add_argument('--setWaveFormCycleNumber',
                        type=int,
                        help='''Set the waveform cycle number
                        amount of times given waveform will perform
                        cycleNum: 0 -> unlimited times''')
    parser.add_argument('--startWaveForm',
                        action='store_true',
                        help='start waveform')
    parser.add_argument('--stopWaveForm',
                        action='store_true',
                        help='stop waveform')
    parser.add_argument('--getU',
                        action='store_true',
                        help='print Voltage')
    parser.add_argument('--getI',
                        action='store_true',
                        help='print Current')
    parser.add_argument('--getOut',
                        action='store_true',
                        help='print if the power is on or off')
    parser.add_argument('--hwversion',
                        action='store_true',
                        help='print version returned by SSP_9081')


    args = parser.parse_args()

    if args.port is None:
        print("Error: Port is not specified (can use ENV_VAR 'SSP_9081')")
        exit(RET_WRONG_SETTINGS)

    com = SSP_9081_Serial(args.port)
    power = SSP_9081(com)

    if args.getOut:
        print("Out: ", power.getOut())

    if args.off:
        print("setOff: ", power.setOut(False))

    if args.setI is not None:
        print("setI({}A): ".format(args.setI), power.setI(args.setI))

    if args.setU is not None:
        print("setU({}V): ".format(args.setU), power.setU(args.setU))

    if args.getU:
        print("getU: ", power.getU())

    if args.getI:
        print("getI: ", power.getI())

    if args.on:
        print("setOn: ", power.setOut(True))
    
    if args.setWaveForm is not None:
        print("setWaveForm: ", power.waveForm.loadCSV(args.setWaveForm))

    if args.setWaveFormCycleNumber is not None:
        print("setWaveFormCycleNumber: ", power.waveForm.setCycleNumber(args.setWaveFormCycleNumber))
        
    if args.startWaveForm:
        if not power.getOut():
            print("setOn: ", power.setOut(True))
        print("setWaveFormOn: ", power.waveForm.start())
    
    if args.stopWaveForm:
        print("setWaveFormOff: ", power.waveForm.stop())

    if args.hwversion:
        print("Version: ", power.getVersion())

    if args.waitU is not None and args.setU is not None:
        start_time = time.time()
        import math
        while True:
            U = power.getU()
            if math.isclose(args.setU, U, abs_tol=0.5):
                print("U = ", U)
                print(time.time() - start_time, 's')
                break
            if args.waitU > 0.0:
                if time.time() - start_time >= args.waitU:
                    ret_code = RET_TIMEOUT
                    print("U = ", U)
                    print("Timeout")
                    break
            time.sleep(0.5)

    power.close()

    exit(ret_code)

