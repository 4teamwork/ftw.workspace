from Products.PloneTestCase import ptc
from collective.testcaselayer import ptc as tcl_ptc
from collective.testcaselayer import common

class Layer(tcl_ptc.BasePTCLayer):
    """Install ftw.workspace"""

    def afterSetUp(self):
        ptc.installPackage('ftw.workspace')
        self.addProfile('ftw.workspace:default')

layer = Layer([common.common_layer])
