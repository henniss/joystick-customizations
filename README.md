# joystick-customizations

My personal user plugins for JoystickGremlin. This is not an officially supported Google product.

## Manager

Due to https://github.com/WhiteMagic/JoystickGremlin/issues/309, JoystickGremlin
only supports a single instance of the periodic decorator. As a hacky
workaround, I use one instance of this manager plugin to manage all the polling
for my plugins. 

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
at the start of a sortie) . In this case, moving the axis momentarily to its
lower limit will resync them.

## Setup

Copy all three .py files into a directory you intend to use for your joystick
gremlin plugins.

Within joystick gremlin, add one instance of the manager plugin. It shouldn't
need any adjustment.

Create at least three modes: one for bf 110s, one for spitfires and he 111s, and
one for all other planes. Use joystick gremlin to bind switch-mode to
appropriate keys (I use a five-position selector on my throttle).

Now import the discrete-axis plugin, and click '+' to add three more instances
of it. Set them up as follows:

```
mode        axis     buttons     N

spit/111   water     1/2         6

spit/111   oil       3/4         5

110        water     1/2         9

110        oil       3/4         5

```


Save and activate your profile. Open up the input viewer and verify that these
button presses can be seen as you move these axes. 

If so, launch the sim and bind buttons 1/2/3/4 to the appropriate oil/water
open/closed actions by wiggling the axis.

## Bugs

https://github.com/WhiteMagic/JoystickGremlin/issues/239

It's necessary to activate, deactivate, and activate again the profile for it to
take effect.  It is necessary to do this each time you launch joystick gremlin.
