#!python3
__version__ = "1.0.11"

# import ssp_9081
import argparse
import os

from ssp_9081.interfaces import SSP_9081_Serial
from ssp_9081 import SSP_9081


def main():
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
        exit(1)

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

    if args.hwversion:
        print("Version: ", power.getVersion())

    power.close()

