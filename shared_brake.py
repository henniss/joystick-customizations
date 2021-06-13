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

import sys
import math
import os

l_axis=PhysicalInputVariable(
    'left_brake',
    'Left toe brake',
    [gremlin.common.InputType.JoystickAxis]
)
r_brake=PhysicalInputVariable(
    'right_brake',
    'Right toe brake',
    [gremlin.common.InputType.JoystickAxis]
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

mixer_mode = "scaled"
    
p_decorator = l_brake.create_decorator(mode.value)
s_decorator = r_brake.create_decorator(mode.value)

@p_decorator.axis(l_brake.input_id)
def axis_change(event, vjoy):
    v_p = event.value
    v_s = read_axis(r_brake)
    x = mix(v_p, v_s)
    set_out(x, vjoy)
    
@s_decorator.axis(l_brake.input_id)
def axis_change(event, vjoy):
    lb = event.value
    rb = read_axis(l_brake)
    x = mix(lb,rb)
    set_out(x, vjoy)

def mix(l, r):
    return (l + r) / 2

def read_axis(axis):
    device = joy[axis.value['device_id']]
    _axis = device.axis(axis.value['input_id'])
    return _axis.value

def set_out(x, vjoy):
    device = vjoy[v_axis.value['device_id']]
    axis = device.axis(v_axis.value['input_id'])
    axis.value = x
