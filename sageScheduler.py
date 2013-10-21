import sageGateBase as sgb
import wx, socket, xmlrpclib, sys
from globals import *
import traceback as tb

####################################################################
#
# DESCRIPTION: The class will allow for the scheduling of apps on a
#              SAGE wall.
#              
#
# DATE: Oct, 2013
#
####################################################################

class SageScheduler(sgb.SageGateBase):

	def __init__(self):
        sgb.SageGateBase.__init__(self,
                                  sageServerHost=getSAGEServer(),
                                  useAppLauncher=True,
                                  forceAppLauncher=getAppLauncher(),
                                  onDisconnect=self.initiateClosedConnectionDialog,
                                  verbose=True)
