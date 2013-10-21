
############################################################################
#
#  IMPORTS
#
############################################################################

# python and wx stuff
import string, sys, os, copy, optparse, time
from threading import Timer
import traceback as tb

# hyperlink module is not (yet) included with wxPython as a standard module
# so not all distributions have it
global use_hyperlink
use_hyperlink = True
try:
    import wx.lib.hyperlink as hyperlink    #for the about box
except:
    use_hyperlink = False

# if this UI should autosave
global autosave

# my stuff
import Graph
from sageGate import *
from sageData import *
from canvases import *
from globals import *
from users import * 
import preferences as prefs
import launcherAdmin as lAdmin
from sagePath import getUserPath

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
		                          
  	def getAppList(self):
  		return self.appLauncher.getAppList(self);
  		
  		
############################################################################
#
# Main entry point for the application
#
############################################################################

### sets up the parser for the command line options
def get_commandline_options():
    parser = optparse.OptionParser()

    h = "if set, prints output to console, otherwise to ~/.sageConfig/sageui/output_log.txt"
    parser.add_option("-v", "--verbose", action="store_true", help=h, dest="verbose", default=False)

    h = "which sage server / connection manager to use (default is sage.sl.startap.net)"
    parser.add_option("-s", "--server", dest="server", help=h, default="sage.sl.startap.net")

    h = "change the port number of the sage server (default is 15558)"
    parser.add_option("-p", "--port", help=h, type="int", dest="port", default=15558)

    h = "override which application launcher to use (by default it looks for one on the same machine as sage master. Specify as machine:port)"
    parser.add_option("-l", "--launcher", dest="launcher", help=h, default="")

    h = "try autologin to this sage name (what fsManager reports to connection manager from fsManager.conf )"
    parser.add_option("-a", "--autologin", dest="autologin", help=h, default=None)

    h = "upon startup load this saved state (write saved state name from saved-states directory)"
    parser.add_option("-o", "--load_state", dest="load_state", help=h, default=None)

    h = "perform autosave?"
    parser.add_option("-t", "--autosave", action="store_true", help=h, dest="autosave", default=False)

    return parser.parse_args()



def main(argv):
    os.chdir(sys.path[0])  # change to the folder where script is running
    global autosave
    verbose = False
    usersServerIP = "74.114.99.36"
    usersServerPort = 15558
    
    # parse the command line params
    (options, args) = get_commandline_options()
    verbose = options.verbose
    usersServerPort = options.port
    usersServerIP = options.server
    appLauncher = options.launcher
    autologinMachine = options.autologin
    loadState = options.load_state
    autosave = options.autosave
    
    # set the overridden app launcher
    if appLauncher != "":
        setAppLauncher(appLauncher)
        
    # set the global variable for the SAGE SERVER
    setSAGEServer(usersServerIP)
    
    # print some information about the system currently running
    print "\nCurrently running:\n--------------------------"
    print "SAGE UI version: ", VERSION
    print "Python version:  ", string.split(sys.version, "(", 1)[0]
    print "wxPython version: "+str(wx.VERSION[0])+"."+str(wx.VERSION[1])+"."+str(wx.VERSION[2])+"."+str(wx.VERSION[3])+"\n"  

    # read all the preferences
    import preferences as prefs
    prefs.readAllPreferences()

    app = SAGEui(usersServerIP, usersServerPort, verbose, autologinMachine, loadState)
    app.MainLoop()
    
    


if __name__ == '__main__':
    import sys, os
    main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])


    
    


