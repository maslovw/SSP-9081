from unittest import TestCase
from ssp_9081.ssp_9081_interfaces import SSP_9081_Serial
from ssp_9081 import SSP_9081
from time import sleep

class TestSSP_9081_Serial(TestCase):
    def setUp(self):
        self.ifc = SSP_9081_Serial('COM3')
        self.cut = SSP_9081(self.ifc)

    def test_TurnPowerOn(self):
        self.cut.setOut(True)
        sleep(1)
        self.assertTrue(self.cut.getOut())

    def test_TurnPowerOff(self):
        self.cut.setOut(False)
        sleep(1)
        self.assertFalse(self.cut.getOut())

    def test_set_12V(self):
        self.assertTrue(self.cut.getOut())
        self.cut.setU(12.)
        self.assertEqual(self.cut.getPresetUI(0)[0], 12.)
        sleep(5)
        self.assertGreaterEqual(self.cut.getU(), 11.)

    def test_set_5V(self):
        self.assertTrue(self.cut.getOut())
        self.cut.setU(5.)
        self.assertEqual(self.cut.getPresetUI(0)[0], 5.)
        sleep(5)
        self.assertGreaterEqual(self.cut.getU(), 4.5)
        self.assertGreaterEqual(self.cut.getU(), 4.5)


