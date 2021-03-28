
from gremlin.util import log

callbacks = []

def register_vjoy_callback(fn):
    global callbacks
    callbacks.append(fn)
    
    
def do_callbacks(vjoy):
    global callbacks
    for cb in callbacks:
        cb(vjoy)
        
        
@register_vjoy_callback
def do_log(vjoy):
    log("Callbacks started")