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

# Notes:

# Even more so than the other files in this repo, this was written for
# my own specific needs, with no attention paid to making something
# generic. I have no idea if it can be made to work with devices that
# aren't a nanoKONTROL2.

# (IOW, this code is crap: deal with it)

# With the nanoKontrol2, you will need to set the appropriate mode
# (see Operation Mode in the manual). IIRC this is the "CYCLE" mode,
# but TBH I set this up about a year ago and haven't touched it since,
# so I'm not certain.

# You'll also need to make sure pygame is installed, of course. 

# I haven't made any attempt to make this customizable within the JG
# UI. Any customization for other devices will need to be done in
# code. I recommend writing a simple loop with pygame to print out all
# events so you can see what codes are reported.

# JG doesn't seem to have provision for a virtualenv on its own, so
# activate one (for pygame)
venv_py = "./venv/bin/activate_this.py"
exec(open(venv_py).read(), {'__file__': venv_py}).

import enum
import collections
import functools

import pygame
import pygame.midi as pm

import gremlin
from gremlin.user_plugin import *
from gremlin.util import log

import sys
import os
# Patch path to allow us to import a module installed next to this file.
try:
    import pollmanager
except ImportError:
    sys.path.append(os.path.dirname(__file__))
    import pollmanager



class MixerMode(enum.Enum):
    RAW = 0
    MIN = 1
    BLENDED = 2

mode_map = {**{i: MixerMode.BLENDED for i in [32,33,34,35]},
            **{i: MixerMode.MIN for i in [48,49,50,51]},
            **{i: MixerMode.RAW for i in [64,65,66,67]}}

class EngineMixer:

    def __init__(self, name, vjoy_code):
        self.name = name
        self._vjoy_code = vjoy_code

        self.primary = 1
        self.secondary = 1
        self.mode = MixerMode.BLENDED

        self.updated = True

    def set_primary(self, x):
        # jg input ranges from -1 to 1
        self.primary = (1 + x)/2
        self.updated = True

    def set_secondary(self, x):
        # nanoKontrol input ranges from 0 to 127
        self.secondary = x / 127
        self.updated = True

    def set_mode(self, mode):
        self.updated = True
        print(f"{self.name} becomes {mode}")
        self.mode = mode

    def send_output(self, vjoy):
        if not self.updated:
            return

        if self.mode == MixerMode.BLENDED:
            val = self.primary * self.secondary
        elif self.mode == MixerMode.MIN:
            val = min(self.primary, self.secondary)
        elif self.mode == MixerMode.RAW:
            val = self.secondary
        # normalize range to [-1, 1]
        val = (2 * val) - 1
        # print(f"{self.name}: {val}")
        dev, ax = self._vjoy_code
        vjoy[dev].axis(ax).value = val
        self.updated = False

AXIS_MAP = collections.defaultdict(list)
def register_axis(id, f):
    AXIS_MAP[id].append(f)

BUTTON_MAP = collections.defaultdict(list)
def register_button(id, f):
    BUTTON_MAP[id].append(f)

SYSTEMS=['throttle', 'rpm', 'mixture', 'radiator']
# second argument customizes vjoy device controlled
MIXERS = {
    'throttle': {
        1+i: EngineMixer(f"throttle{i+1}", (1,4+i))
        for i in range(0, 4)},
    'rpm': {
        1+i: EngineMixer(f"rpm{i+1}", (2,1+i))
        for i in range(0, 4)},
    'mixture': {
        1+i: EngineMixer(f"mixture{i+1}", (4,1+i))
        for i in range(0, 4)},
    'radiator': {
        1+i: EngineMixer(f"radiator{i+1}", (4,5+i))
        for i in range(0, 4)},
    }
# register axes
for i in range(0, 4):
    register_axis(i, MIXERS["throttle"][i+1].set_secondary)
    register_axis(4+i, MIXERS["rpm"][i+1].set_secondary)
    register_axis(16+i, MIXERS["mixture"][i+1].set_secondary)
    register_axis(20+i, MIXERS["radiator"][i+1].set_secondary)
# register set mode buttons
for base, mode in zip([32, 48, 64], [MixerMode.BLENDED, MixerMode.MIN,
                                     MixerMode.RAW]):
    for i in range(0, 4):
        for system in SYSTEMS:
            register_button(
                base + i,
                functools.partial(MIXERS[system][i+1].set_mode, mode))

AXIS_MAP=dict(AXIS_MAP)
BUTTON_MAP=dict(BUTTON_MAP)

MAX_EVENTS=100
def process_events(device, vjoy):
    if device.poll():
        for event, _ in device.read(MAX_EVENTS):
            req, id, val, _ = event
            if req != 176:
                # I don't know why this is always 176, but that seems
                # requried
                continue
            if id in AXIS_MAP:
                for f in AXIS_MAP[id]:
                    f(val)
            if id in BUTTON_MAP:
                for f in BUTTON_MAP[id]:
                    f()
        for i in range(0, 4):
            for system in SYSTEMS:
                MIXERS[system][i+1].send_output(vjoy)

pygame.midi.init()

def get_device_id(name, kind='input'):
    if kind not in ('input', 'output'):
        raise ValueError("Unrecognized kind %s." % kind)
    N=pm.get_count()
    print(N)
    for i in range(N):
        _, dev_name, input, output, _ = pm.get_device_info(i)
        if kind == 'input' and input != 1:
            continue
        if kind == 'output' and output != 1:
            continue
        if name == dev_name:
            return i
    raise KeyError("Couldn't find device %s." % name)

DEVICE=pm.Input(get_device_id(b'nanoKONTROL2 MIDI 1', 'input'))
@pollmanager.register_vjoy_callback
def do_poll(vjoy):
    process_events(DEVICE, vjoy)

cm3 = gremlin.input_devices.JoystickDecorator("Virpil CM3", "TODO", "quad")
twcs = gremlin.input_devices.JoystickDecorator("TWCS", "TODO", "quad")
trim = gremlin.input_devices.JoystickDecorator("Trim Box", "TODO", "quad")

@cm3.axis(3)
def lthrottle(event, vjoy):
    mixers = [MIXERS['throttle'][i] for i in [1, 2]]
    joystick_event(event.value, mixers, vjoy)

@cm3.axis(4)
def rthrottle(event, vjoy):
    mixers = [MIXERS['throttle'][i] for i in [3,4]]
    joystick_event(event.value, mixers, vjoy)

@cm3.axis(5)
def rpm(event, vjoy):
    mixers = [MIXERS['rpm'][i] for i in [1, 2,3,4]]
    joystick_event(event.value, mixers, vjoy)

@trim.axis(4)
def rpm(event, vjoy):
    mixers = [MIXERS['mixture'][i] for i in [1, 2,3,4]]
    joystick_event(event.value, mixers, vjoy)

@twcs.axis(3)
def rpm(event, vjoy):
    mixers = [MIXERS['radiator'][i] for i in [1, 2,3,4]]
    joystick_event(event.value, mixers, vjoy)

def joystick_event(val, mixers, vjoy):
    """Generic handler for all the normal joystick event handlers"""
    for m in mixers:
        m.set_primary(
    for m in mixers:
        m.send_output(vjoy)
