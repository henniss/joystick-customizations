import gremlin
import math
from gremlin.user_plugin import *
from gremlin.util import log

from time import sleep

import sys
import os

# Patch path to allow us to import a module installed next to this file.
try:
    import pollmanager
except ImportError:
    sys.path.append(os.path.dirname(__file__))
    import pollmanager
    
    
# Spitfire -- Water: 6
# He 111   -- Oil  : 5
# bf 110   -- Water: 9
# bf 110   -- Oil  : 5
N = IntegerVariable(
    'N',
    'Number of discrete values to partition the axis into',
    initial_value=6,
    min_value=1,
    max_value=100,)

# Allow some amount of hysteresis so that a noisy axis positioned right near a boundary point doesn't jitter back and forth. 
overlap = IntegerVariable(
    'overlap',
    'Scale regions by this factor, to allow some hysteresis.',
    initial_value=5,
    min_value=0,
    max_value=100,
)

# Il-2 seems to require this be > 0. I'm not sure what the limit is, but 50 seems to be a reasonable choice. 
delay = IntegerVariable(
    'Delay',
    'Number of ms to hold button presses.',
    initial_value=50,
    min_value=0,
    max_value=100)
# poll_freq = IntegerVariable(
    # 'Polling Frequency',
    # 'Number of ms between polling. Recommended: twice delay.',
    # initial_value=100,
    # min_value=0,
    # max_value=200)
    
p_axis=PhysicalInputVariable(
    'Axis',
    'Joystick axis which will be discretized',
    [gremlin.common.InputType.JoystickAxis]
)
v_up=VirtualInputVariable(
    "Up",
    "vJoy button to press when incrementing the axis.",
    [gremlin.common.InputType.JoystickButton]
)
v_down=VirtualInputVariable(
    "Down",   
    "vJoy button to press when decrementing the axis.",
    [gremlin.common.InputType.JoystickButton]
)

# You'll want to use this to switch between different values of N for different planes. 
mode = ModeVariable(
        "Mode",
        "The mode to use for this mapping"
)

value = -1
step = 0
reset_low = False
already_reset = False

def get_candidates(value):
    """Find possible discrete values that could correspond to the given axis value.
    
    For some axis values, there are multiple steps this value could correspond to. This finds all such values. 
    """
    # N settings means center-points are at
    # -1 + 2*i/(N-1)
    # It follows that dividing points are at
    # -1 + (2 * i - alpha) / (N - 1) # lower, (
    # -1 + (2 * i + alpha) / (N - 1) # upper, )
    
    # Thus, we want to find the largest ( below, and the smallest )
    # above.

    #  ((N-1)(v+1) + alpha) / 2 > i
    # ((N-1)(v+1) - alpha) / 2 < i
    _N = N.value
    v = value
    alpha = 1 + overlap.value / 100
    i_low = math.floor(((_N-1)*(v + 1) + alpha) / 2)
    i_high = math.ceil(((_N-1)*(v + 1) - alpha) / 2)
    x_low = -1 + (2 * i_low - alpha) / (_N - 1)
    x_high = -1 + (2 * i_high + alpha) / (_N - 1)
    # log(f"high: {i_high}, low : {i_low }")
    # log(f"x_high: {x_high}, x_low: {x_low}")
    return set((i_low , i_high))
    
axis_decorator = p_axis.create_decorator(mode.value)
# log("Init")


@axis_decorator.axis(p_axis.input_id)
def axis_change(event, vjoy):
    global step, value, reset_low, already_reset
    value = event.value
    if value == -1:
        if not already_reset:
            reset_low = True
            already_reset = True
            step = N.value
    else:
        already_reset = False

# Due to https://github.com/WhiteMagic/JoystickGremlin/issues/309
# we can't have multiple instances using the periodic decorator. As a hacky workaround, 
# the manager plugin registers a single periodic callback, 
# which executes all of the callbacks registered by instances of this plugin. 

#@gremlin.input_devices.periodic(poll_freq.value / 1000)
@pollmanager.register_vjoy_callback
def poll(vjoy):
    global step, reset_low, value
    # log("polling")
    # Make sure that even if things get out of sync, moving the axis
    # to the low stop resets it to the lowest setting.
    if reset_low:
        # log("resetting")
        down(vjoy)
        if step <= 0:
            reset_low = False
            # log("done resetting")
        return

    candidates = get_candidates(value)
    if step in candidates:
        # log("Nothing to do")
        return

    if step < min(candidates):
        # log("up")
        up(vjoy)
    elif step > max(candidates):
        # log("down")
        down(vjoy)
    else:
        log("Go fix your get_candidates function!")
        assert False

def short_press(button):
    button.is_pressed=True
    sleep(delay.value / 1000)
    button.is_pressed=False
    
def up(vjoy):
    global step
    device = vjoy[v_up.value['device_id']]
    button = device.button(v_up.value['input_id'])
    short_press(button)
    step += 1

def down(vjoy):
    global step
    device = vjoy[v_down.value['device_id']]
    button = device.button(v_down.value['input_id'])
    short_press(button)
    step -= 1
    
