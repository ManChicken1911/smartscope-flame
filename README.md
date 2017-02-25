# SmartScope-Flame Controller
by Bob Maple (bobm-matchbox [at] idolum.com)

This script is licensed under the Creative Commons Attribution-ShareAlike [CC BY-SA](https://creativecommons.org/licenses/by-sa/4.0/)


## What

This Python hook controls a Blackmagic Design SmartScope Duo 4K from Autodesk Flame,
allowing you to switch what each monitor is displaying from a variety of presets.

SmartScope-Flame Controller uses a Python hook in Autodesk Flame/Flame Assist/Flare
to add a "SmartScope Duo" context menu in the application.  Communication is done
via Ethernet, so your SmartScope must be on the network.


## Installing

### Flame 2018 and above

Autodesk has changed the way hooks are loaded in Flame 2018 and it's now much simpler
to install the SmartScope-Flame Controller. All you need to do is drop it into the
Flame 2018 install's python directory:

  `sudo cp ./smartscope-control.py /opt/Autodesk/flame_2018/python`

and then either relaunch Flame or use the hotkey Shift-Control-H-P to reload all
the Python hooks.

### Flame 2016 and 2017

To install in Flame 2016 or 2017, first place smartscope-flame.py in Flame's python
directory:

  `sudo cp ./smartscope-control.py /usr/discreet/flame_2017.1/python/`

where 'flame_2017.1' will vary depending on your specific application and version.
Technically this script can be placed anywhere but it's convenient to keep it with
the rest of Flame's Python code. Note that you might need to be root to do this.

To connect the code into Flame, open hook.py in a text editor and comment out
the supplied functions getCustomUIActions and customUIAction so they look like:

```
# def getCustomUIActions( ):
#     return ()

...

# def customUIAction( info, userData ):
#     pass
```

Then add a line either after what you just commented out or to the very end of
the file:

  `execfile("/usr/discreet/flame_2017.1/python/smartscope-control.py")`

again replacing `flame_2017.1` with the proper directory name based on your setup,
or if you decided to put the script somewhere else entirely, replace the whole
pathname with the correct location as appropriate.

(NOTE: If you already have existing custom context menu hooks, you'll ignore
everything above and have to just manually integrate the code from the hooks in
smartscope-flame.py into your existing hooks and make it work.)


## Configuring

Edit smartscope-flame.py in a text editor and modify the ssdc_hostname config
variable near the top to tell it how to reach your SmartScope:

```
#### Configuration ####
ssdc_hostname = '192.168.1.1'  # IP or hostname
```
It can be specified as a hostname or IP address (shown.)

### Additional Config

There are some additional configuration variables which you can customize
to your liking.

First there two sets of config variables for setting the screen brightness and
constrast used for Scope displays (Parade, Vector, Waveform, etc) and the Picture
display:

```
ssdc_scope    = { "brightness": "127", "contrast": "127" }
ssdc_picture  = { "brightness": "127", "contrast": "127" }
```
Values are 0-255 with 127 being 'default' (50% Brightness and 100% Contrast in
the SmartView app.)

You can also swap the displays to be opposite of how they are listed in the menu:

```
ssdc_swap     = False
```

Setting this to **True** will swap the left and right displays, so that choosing
"Parade RGB | Vectorscope" will actually display the Vectorscope on the left monitor
and the RGB Parade on the right monitor.


## Using

After the initial install, start or restart Flame.  Or, if it was already running
when you installed, press **Shift-Control-H-P** in Flame to reload the Python hooks.

Right-click somewhere on the Flame desktop (in the Player, Reels, Freeform view,
etc) to pull up the context menu and you should now have a **SmartScope Duo** entry
at the bottom.
