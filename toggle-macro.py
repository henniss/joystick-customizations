import gremlin
import math
from gremlin.user_plugin import *
from gremlin.util import log

from time import sleep

toggle = PhysicalInputVariable(
'Toggle',
'A toggle switch',
[gremlin.common.InputType.JoystickButton],
)
v_on = VirtualInputVariable(
'On',
'vJoy button bound to toggle-on',
[gremlin.common.InputType.JoystickButton],
)
v_off = VirtualInputVariable(
'Off',
'vjoy button bound to toggle-off',
[gremlin.common.InputType.JoystickButton],
)

mode = ModeVariable(
        "Mode",
        "The mode to use for this mapping"
)

toggle_decorator = toggle.create_decorator(mode.value)


@toggle_decorator.button(toggle.input_id)
def flip(event, vjoy):
   off = vjoy[v_off.value['device_id']].button(v_off.value['input_id'])
   on = vjoy[v_on.value['device_id']].button(v_on.value['input_id'])
   
   if event.is_pressed:
       on.is_pressed = True
       sleep(0.1)
       on.is_pressed = False
   else:
       off.is_pressed = True
       sleep(0.1)
       off.is_pressed = False
