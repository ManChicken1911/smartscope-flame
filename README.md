# SmartScope-Flame Controller
by Bob Maple (bobm-matchbox [at] idolum.com)

This script is licensed under the Creative Commons Attribution-ShareAlike [CC BY-SA](https://creativecommons.org/licenses/by-sa/4.0/)

![Flame version 2022+](https://img.shields.io/badge/Flame-2022+-green)

## What

This Python hook controls a Blackmagic Design SmartScope Duo 4K from Autodesk Flame,
allowing you to switch what each monitor is displaying from a variety of presets.

SmartScope-Flame Controller uses a Python hook in Autodesk Flame/Flame Assist/Flare
to add a "SmartScope Duo" context menu in the application.  Communication is done
via Ethernet, so your SmartScope must be on the network.


## Installing

### Flame 2022

Autodesk Flame 2022 has moved to Python 3.7 and SmartScope-Flame has been updated
as a result to match.

All you need to do is drop the script into the Flame shared python directory:

  `sudo cp ./smartscope-control.py /opt/Autodesk/shared/python/`

and then either relaunch Flame or use the hotkey Shift-Control-H-P to reload all
the Python hooks.

### Flame 2020 and 2021

Please see the v1.2 release for compatible script and instructions.


## Configuring

Edit smartscope-control.py in a text editor and modify the ssdc_hostname config
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

Click on the Flame menu in the lower-right corner of the Flame UI and you should
see a new **SmartScope Duo** entry near the top. Just select the desired layout,
or use **Off** to turn off both screens.
