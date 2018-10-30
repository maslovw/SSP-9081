from unittest import TestCase
from ssp_9081.interfaces import SSP_9081_Serial
from ssp_9081 import SSP_9081, SequenceItem
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

    def test_set_waveform(self):
        # self.assertTrue(self.cut.getOut())
        self.assertFalse(self.cut.waveForm.isRunning())
        self.cut.waveForm.setCycleNumber(1)
        self.cut.waveForm.setPointsToRun(6)
        self.cut.waveForm.setStep(SequenceItem(1, 11., 5))
        self.cut.waveForm.setStep(SequenceItem(2, 11., 0))
        self.cut.waveForm.setStep(SequenceItem(3, 4., 5))
        self.cut.waveForm.setStep(SequenceItem(4, 4., 0))
        self.cut.waveForm.setStep(SequenceItem(5, 12., 5))
        self.cut.waveForm.setStep(SequenceItem(6, 12., 0))
        self.cut.setOut(True)
        self.cut.waveForm.start()
        sleep(3)
        self.assertAlmostEqual(11., self.cut.getU(), delta=0.5 )
        sleep(5)
        self.assertAlmostEqual(4., self.cut.getU(), delta=0.5)
        sleep(5)
        self.assertAlmostEqual(12., self.cut.getU(), delta=0.5)
        self.assertTrue(self.cut.waveForm.isRunning())
        sleep(6)
        self.assertFalse(self.cut.waveForm.isRunning())


