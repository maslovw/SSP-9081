from serial import Serial
from time import sleep
from ssp_9081.interfaces import SSP_9081_INTERFACE
import logging


class SSP_9081_Exception(Exception):
    pass

class SSP_9081():
    def __init__(self, interface: SSP_9081_INTERFACE,  logLevel=logging.DEBUG):
        self.connection = interface
        self.waveForm = SSP_9081.WaveForm(self)
        self.logger = logging.getLogger('SSP-9081')
        self.logger.setLevel(logLevel)

    def open(self, **kwargs):
        self.connection.open(**kwargs)

    def close(self):
        self.logger.debug('close')
        self.connection.close()

    def __del__(self):
        self.close()

    def send(self, cmd: str) -> (bool, str):
        """
        :param cmd: python string without CR
        :return: (result: bool, response: str)
        """
        self.logger.debug('send: {}'.format(cmd))
        self.connection.send(cmd)
        return self.connection.recv()


    def getUI(self) -> (float, float):
        res, resp = self.send('GETD')
        if not res or resp is None:
            return None, None
        values =  resp.split(';')
        u = values[0]
        i = values[1]
        mode = values[2]
        self.logger.debug('U: {}, I: {}, Mode: {}'.format(u, i, "CV" if mode == 0 else "CC"))
        return (int(u)/100, int(i)/1000)

    def getU(self) -> float:
        u,_ = self.getUI()
        return u

    def getI(self):
        _,i = self.getUI()
        return i

    def setPresetUI(self, preset:int, voltage:float, current:float):
        assert preset < 4
        v = int(voltage*100)
        i = int(current * 1000)
        res, _ = self.send('SETD{}{:04}{:04}'.format(preset, v, i))
        return res

    def getPresetUI(self, preset:int) -> (float, float):
        """Get Setting preset 0/1/2/3 Volt & Curr
           preset = 0 -> Normal Mode
           return (Voltage, current)
        """
        assert preset < 4, "Only 0,1,2 or 3 available presets"
        res, resp = self.send('GETS{}'.format(preset))
        if not res or resp is None:
            return None, None
        values =  resp.split(';')
        u = values[0]
        i = values[1]
        self.logger.debug('U: {}, I: {}'.format(u, i))
        return (int(u)/100, int(i)/1000)

    def setOut(self, state:bool) -> bool:
        """
        Turning on or off the output
        :param state:
        :return:
        """
        s = 1 if state else 0
        res, _ = self.send('SOUT{}'.format(s))
        return res

    def getOut(self) -> bool:
        """Get Output Status
        return state of the power supply
        :return: True if power is on
        """
        res, resp = self.send('GOUT{}')
        if not res or resp is None:
            raise SSP_9081_Exception("no response")
        return '1' in resp

    def setU(self, voltage, preset=0):
        """Set output Voltage
        :param voltage - float
        :param preset - memory preset
        """
        assert preset < 4
        v = int(voltage*100)
        res, _ = self.send('VOLT{}{:04}'.format(preset, v))
        return res

    def setI(self, current:float, preset=0):
        """Set output Current
        :param current - float
        :param preset - memory preset
        total power <= 80W
        """
        assert preset < 4
        i = int(current * 1000)
        res, _ = self.send('CURR{}{:04}'.format(preset, i))
        return res

    def getPreset(self) -> int:
        """
        Get selected preset
        :return: 0/1/2/3
        """
        res, resp = self.send('GABC{}')
        if not res or resp is None:
            raise SSP_9081_Exception("no response")
        return int(resp)

    def setPreset(self, preset:int) -> bool:
        """
        Set preset number
        :param preset: 0 (Normal Mode), 1 (A), 2(B), 3(C)
        """
        assert preset < 4
        res, _ = self.send('SABC{}'.format(preset))
        return res

    def setKeyboard(self, state: bool) -> bool:
        """Enable/Disable keyboard"""
        if state:
            res, _ = self.send('ENDS') # enable keyboard
        else:
            res, _ = self.send('SESS') # Disable keyboard
        return res

    def setUpperVoltageLimit(self, limit:float):
        v = int(limit*100)
        res, _ = self.send('SOVP{:04}'.format(v))
        return res

    def getUpperVoltageLimit(self) -> float:
        res, resp = self.send('GOVP')
        if not res or resp is None:
            raise SSP_9081_Exception("no response")
        return int(resp)/100

    def getVersion(self) -> str:
        res, resp = self.send('GVER')
        if not res or resp is None:
            raise SSP_9081_Exception("no response")
        return resp

    def getPower(self) -> float:
        res, resp = self.send('GPOW')
        if not res or resp is None:
            raise SSP_9081_Exception("no response")
        return int(resp)/10

    class WaveForm:
        def __init__(self, control: 'SSP_9081'):
            self.control = control

        def setCycleNumber(self, cycleNum: int):
            """
            Set the waveform cycle number
            amount of times given waveform will perform
            cycleNum: 0 -> unlimited times
            """
            assert cycleNum <= 999
            return self.control.send('SWCN{:03}'.format(cycleNum))

        def getCycleNumber(self):
            res, resp = self.control.send('GWCN')
            if not res or resp is None:
                raise SSP_9081_Exception("no response")
            return int(resp)

        def setPointsToRun(self, numberOfPoints):
            """
            :param numberOfPoints: 2-10: amount of steps in one cycle for the waveForm
            """
            assert numberOfPoints >=2 and numberOfPoints <= 10
            return self.control.send('RPOI{:02}'.format(numberOfPoints))

        def getPointsToRun(self) -> int:
            res, resp = self.control.send('GPOI')
            if not res or resp is None:
                raise SSP_9081_Exception("no response")
            return int(resp)

        def setStep(self, seqItem: 'SequenceItem'):
            assert seqItem.number > 0 and seqItem.number <= 10, "point can be in range [1 - 10]"
            cmd = seqItem.to_cmd()
            return self.control.send(cmd)

        def getStep(self, point: int):
            assert point > 0 and point <= 10, "point can be in range [1 - 10]"
            res, resp = self.control.send('GWFP{:02}'.format(point))
            if not res or resp is None:
                raise SSP_9081_Exception("no response")
            return SequenceItem.from_resp(point, resp)

        def isRunning(self):
            res, resp = self.control.send('GWRS')
            if not res or resp is None:
                raise SSP_9081_Exception("no response")
            return int(resp) == 1

        def start(self):
            return self.control.send('RUNP')

        def stop(self):
            return self.control.send('STOP')

        def loadCSV(self, filename):
            """
            loadCSV: format: step(1-10),voltage(0.0 - 36.40V),time(0s - 1200s)
            Example:
            1,12.0,5
            2,2.4,10
            """
            import csv
            max_step = 2
            ret = []
            with open(filename) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for line in csv_reader:
                    self.control.logger.debug(';'.join(line))
                    ret += [self.setStep(SequenceItem.from_csv(';'.join(line)))]
                    max_step = max(max_step, int(line[0]))
            ret += [self.setPointsToRun(max_step)]
            self.control.logger.debug('setPointsToRun {}'.format(max_step))
            return ret

class SequenceItem():
    """
    Waveform point description:
    number: point (1-10)
    voltage
    time: amount of seconds this point will be held
    """
    def __init__(self, number:int, voltage:float, time:int):
        """
        :param number: 1-10
        :param voltage: 0.0 - 36.40V
        :param time: 0s - 1200s
        """
        self.number = number
        self.voltage = voltage #V
        self.time = time #s

    @classmethod
    def from_resp(cls, number, resp):
        res = resp.split(';')
        return SequenceItem(number, int(res[0])/100, res[1])

    def to_cmd(self):
        return "SWFP{:02}{:04}{:04}".format(
            self.number,
            int(self.voltage*100),
            int(self.time)
        )

    @classmethod
    def from_csv(cls, line):
        res = line.split(';')
        return SequenceItem(int(res[0]), float(res[1]), int(res[2]))

    def to_csv(self):
        return "{};{:.2f};{}".format(self.number, self.voltage, self.time)


