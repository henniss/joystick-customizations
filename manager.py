import sys
try:
    import pollmanager
except ImportError:
    sys.path.append(r"C:\Users\Harris Enniss\Desktop\joystick-customizations")
    import pollmanager


import gremlin
from gremlin.user_plugin import *

from gremlin.util import log


poll_freq = IntegerVariable(
    'Polling Frequency',
    'Number of ms between polling. Recommended: twice delay.',
    initial_value=100,
    min_value=0,
    max_value=200)
    
    
    
@gremlin.input_devices.periodic(poll_freq.value / 1000)
def poll(vjoy):
    log("Doing poll")
    pollmanager.do_callbacks(vjoy)