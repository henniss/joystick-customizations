# joystick-customizations

My personal user plugins for JoystickGremlin.

## Discrete Axis

Il-2 BoX uses keypresses to move certain axes through a fixed number of
positions. For example, the water radiators on the Spitfire are of this
type. This is inconvienient, since it means you can't control these radiators
with your ordinary water-radiator axis, and you can't get tactile feedback for
where your axis is positioned.

This plugin fixes that, by letting you bind an axis to a pair of up/down
buttons. It keeps track of the current position that the game sees, and
simulates button presses to adjust the radiator in game.

It is possible for the physical and game axes to get out of sync (for instance,
at the start of a sortie) . In this case, moving the axis to its lower limit
will resync them.

## Bugs

https://github.com/WhiteMagic/JoystickGremlin/issues/309

Right now, it's only possible to use one instance of this at a time.

https://github.com/WhiteMagic/JoystickGremlin/issues/239

It's necessary to activate, deactivate, and activate again the profile for it to take effect.
