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


import sys
import os

# Patch path to allow us to import a module installed next to this file.
try:
    import pollmanager
except ImportError:
    sys.path.append(os.path.dirname(__file__))
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
