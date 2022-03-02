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



from gremlin.util import log

callbacks = []

def register_vjoy_callback(fn):
    global callbacks
    callbacks.append(fn)


def do_callbacks(vjoy):
    global callbacks
    for cb in callbacks:
        cb(vjoy)


#@register_vjoy_callback
def do_log(vjoy):
   pass
