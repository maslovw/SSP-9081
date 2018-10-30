from unittest import TestCase
from ssp_9081.ssp_9081_interfaces import SSP_9081_INTERFACE
from ssp_9081.control import SSP_9081

class SSP_9081_Test(SSP_9081_INTERFACE):
    def __init__(self):
        self.cmd = ""
        self.resp = ""

    def send(self, cmd):
        self.cmd = cmd
        return True

    def recv(self):
        return True, self.resp

# power = SSP_9081('COM3')


class TestSSP_9081(TestCase):

    def setUp(self):
        self.ifc = SSP_9081_Test()
        self.cut = SSP_9081(self.ifc)

    def test_getUI(self):
        self.ifc.resp = "500;1000;0;"
        u,i = self.cut.getUI()
        self.assertEqual(self.ifc.cmd, "GETD")
        self.assertEqual(u, 5.0)
        self.assertEqual(i, 1.0)
