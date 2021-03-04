import math
import sys

import gremlin
from gremlin.user_plugin import *
from gremlin.util import log



mode = ModeVariable(
        "Mode",
        "The mode to use for this mapping"
)

N = IntegerVariable(
    'N',
    'Number of ticks on an encoder which should map to the full axis range.'
    initial_value=10,
    min_value=2,
    max_value=sys.maxint)
    
up=PhysicalInputVariable(
    'Up',
    'Encoder direction which increments the axis',
    [gremlin.common.InputType.JoystickButton]
)
down=PhysicalInputVariable(
    'Down',
    'Encoder direction which decrements the axis',
    [gremlin.common.InputType.JoystickButton]
)
vaxis=VirtualInputVariable(
    "Axis",   
    "vJoy axis to manipulate.",
    [gremlin.common.InputType.JoystickAxis]
)

value = -1
    
up_decorator = up.create_decorator(mode.value)
down_decorator = down.create_decorator(mode.value)

@up_decorator.axis(up.input_id)
def axis_change(event, vjoy):
    global value
    if event.is_pressed:
        value = min(value + 2/N.value, 1)
    setaxis(vjoy, value)

@down_decorator.axis(down.input_id)
def axis_change(event, vjoy):
    global value
    if event.is_pressed:
        value = max(value - 2/N.value, -1)
    setaxis(vjoy, value)

def setaxis(vjoy, value):
    device = vjoy[vaxis.value['device_id']]
    axis = device.axis(vaxis.value['input_id'])
    axis.value = value
    
