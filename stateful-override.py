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

from datetime import now

# This is intended to model normally-automatic controls that can be
# overridden in an emergency. Think of a four-way ON-OFF-(ON)-(ON)
# toggle controlling prop pitch (AUTO/MANUAL/COARSE/FINE), or certain
# radiators.

# The intent here is that one key (override) is bound to 'toggle
# auto/manual', and a two-way toggle is bound to up/down.

# Ordinarily, Il-2 makes it easy to lose track of the state of this
# override. This plugin thus tracks state, and only toggles the
# override ON the first time up/down are pressed, and then turns it
# off when the override key is pressed.

# ----

# Il-2 seems to require this be > 0. I'm not sure what the limit is, but 50 seems to be a reasonable choice. 
DELAY=50

# Time after which holding the override key causes a second
# toggle. Useful if our state gets out of sync with the game.
HOLD_SECONDs=2

# Todo: I should create a RESET mixin that lets all instances be reset
# at once.

OVERRIDE=False
Clock=None

key_up = PhysicalInputVariable(
   'Up',
   'Up',
   [gremlin.common.InputType.JoystickButton],
)
key_down = PhysicalInputVariable(
   'Down',
   'Down',
   [gremlin.common.InputType.JoystickButton],
)
key_override = PhysicalInputVariable(
   'Override',
   'Override',
   [gremlin.common.InputType.JoystickButton],
   )

v_up = VirtualInputVariable(
   'Up',
   'Up',
   [gremlin.common.InputType.JoystickButton],
)
v_down = VirtualInputVariable(
   'Down',
   'Down',
   [gremlin.common.InputType.JoystickButton],
)
v_override = VirtualInputVariable(
   'Override',
   'Override',
   [gremlin.common.InputType.JoystickButton],
   )

mode = ModeVariable(
        "Mode",
        "The mode to use for this mapping"
)
up_decorator = key_up.create_decorator(mode.value)
down_decorator = key_down.create_decorator(mode.value)
override_decorator = key_override.create_decorator(mode.value)

def short_press(button):
    button.is_pressed=True
    sleep(DELAY / 1000)
    button.is_pressed=False

def toggle_override(vjoy):
   global OVERRIDE
   OVERRIDE=True
   device = vjoy[v_override.value['device_id']]
   button = device.button(v_override.value['input_id'])
   short_press(button)

@up_decorator.button(key_up.input_id)
def up(event, vjoy):
   global OVERRIDE
   device = vjoy[v_up.value['device_id']]
   button = device.button(v_up.value['input_id'])
   if event.is_pressed:
      if not OVERRIDE:
          toggle_override(vjoy)
      button.is_pressed=True
   else:
      button.is_pressed=False

@down_decorator.button(key_down.input_id)
def down(event, vjoy):
   global OVERRIDE
   device = vjoy[v_down.value['device_id']]
   button = device.button(v_down.value['input_id'])
   if event.is_pressed:
      if not OVERRIDE:
          toggle_override(vjoy)
      button.is_pressed=True
   else:
      button.is_pressed=False

@override_decorator.button(key_override.input_id)
def down(event, vjoy):
   global OVERRIDE, CLOCK
   if event.is_pressed:
      CLOCK=datetime.now()
      if OVERRIDE:
          toggle_override(vjoy)
   elif CLOCK is not None and (CLOCK-time.now()).seconds > HOLD_SECONDS:
      toggle_override(vjoy)

