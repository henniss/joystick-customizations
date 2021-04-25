#Copyright 2021 Google LLC

#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at

#https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied
# See the License for the specific language governing permissions and
# limitations under the License.

import gremlin
import math
from gremlin.user_plugin import *
from gremlin.util import log

from time import sleep


steps = IntegerVariable(
    'steps',
    'Number of encoder-ticks corresponding to full motion of the axis.',
    initial_value=20,
    min_value=1,
    max_value=128)
key_up = PhysicalInputVariable(
'Up',
'Encoder direction corresponding to an increase in the axis.',
[gremlin.common.InputType.JoystickButton],
)
key_down = PhysicalInputVariable(
'Down',
'Encoder direction corresponding to a decrease in the axis.',
[gremlin.common.InputType.JoystickButton],
)
v_axis = VirtualInputVariable(
'axis',
'vJoy axis to manipulate.',
[gremlin.common.InputType.JoystickAxis],
)

mode = ModeVariable(
        "Mode",
        "The mode to use for this mapping"
)

value = -1

up_decorator = key_up.create_decorator(mode.value)
down_decorator = key_down.create_decorator(mode.value)


@up_decorator.button(key_up.input_id)
def up(event, vjoy):
   global value
   #log("up")
   if event.is_pressed:
       value = min(1, value + 2/steps.value)
       set_axis(vjoy, value)
       #log(f"set: {value}")

@down_decorator.button(key_down.input_id)
def down(event, vjoy):
    global value
    if event.is_pressed:
        value = max(-1, value - 2/ steps.value)
        set_axis(vjoy, value)
        # log(f"set: {value}")
        
def set_axis(vjoy, x):
    device = vjoy[v_axis.value['device_id']]
    axis= device.axis(v_axis.value['input_id'])
    axis.value = x
