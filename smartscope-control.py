#!/bin/env python
# ******************************************************************************
#
# SmartScope Duo Controller for Flame v1.1
# Copyright (c) 2015-2017 Bob Maple (bobm-matchbox [at] idolum.com)
#
# Adds a context menu to switch the monitors of the Blackmagic Design
# SmartScope Duo 4K


#### Configuration ####
ssdc_hostname = '192.168.1.1'  # IP or hostname

# Separate Brightness and Contrast values for Scope displays vs Picture
# Ranges 0-255 with 127 being the 'middle' or default value
ssdc_scope    = { "brightness": "127", "contrast": "127" }
ssdc_picture  = { "brightness": "127", "contrast": "127" }

# Swap the left and right monitors
ssdc_swap     = False

####


import time

# Build the context menu and return it to Flame
#
# mon_a is the left display, mon_b is the right display
# The possible modes for each display can be found in the
# SmartScope Manual in the Developer Information section.

def getCustomUIActions( ):

  ssdc1 = {}
  ssdc1[ "name" ] = "ssdcfunc"
  ssdc1[ "caption" ] = "Parade RGB | Vectorscope"
  ssdc1[ "config" ] = { \
  "mon_a": "ParadeRGB", "mon_a_br": ssdc_scope['brightness'], "mon_a_cn": ssdc_scope['contrast'], \
  "mon_b": "Vector75",  "mon_b_br": ssdc_scope['brightness'], "mon_b_cn": ssdc_scope['contrast']  \
  }

  ssdc2 = {}
  ssdc2[ "name" ] = "ssdcfunc"
  ssdc2[ "caption" ] = "Parade RGB | Picture"
  ssdc2[ "config" ] = { \
  "mon_a": "ParadeRGB", "mon_a_br": ssdc_scope['brightness'],   "mon_a_cn": ssdc_scope['contrast'],  \
  "mon_b": "Picture",   "mon_b_br": ssdc_picture['brightness'], "mon_b_cn": ssdc_picture['contrast'] \
  }

  ssdc3 = {}
  ssdc3[ "name" ] = "ssdcfunc"
  ssdc3[ "caption" ] = "Parade YUV | Vectorscope"
  ssdc3[ "config" ] = { \
  "mon_a": "ParadeYUV", "mon_a_br": ssdc_scope['brightness'], "mon_a_cn": ssdc_scope['contrast'], \
  "mon_b": "Vector75",  "mon_b_br": ssdc_scope['brightness'], "mon_b_cn": ssdc_scope['contrast']  \
  }

  ssdc4 = {}
  ssdc4[ "name" ] = "ssdcfunc"
  ssdc4[ "caption" ] = "Parade YUV | Picture"
  ssdc4[ "config" ] = { \
  "mon_a": "ParadeYUV", "mon_a_br": ssdc_scope['brightness'],   "mon_a_cn": ssdc_scope['contrast'],  \
  "mon_b": "Picture",   "mon_b_br": ssdc_picture['brightness'], "mon_b_cn": ssdc_picture['contrast'] \
  }

  ssdc5 = {}
  ssdc5[ "name" ] = "ssdcfunc"
  ssdc5[ "caption" ] = "Waveform | Picture"
  ssdc5[ "config" ] = { \
  "mon_a": "WaveformLuma", "mon_a_br": ssdc_scope['brightness'], "mon_a_cn": ssdc_scope['contrast'],    \
  "mon_b": "Picture",      "mon_b_br": ssdc_picture['brightness'], "mon_b_cn": ssdc_picture['contrast'] \
  }

  ssdc6 = {}
  ssdc6[ "name" ] = "ssdcfunc"
  ssdc6[ "caption" ] = "Audio Dbfs | Histogram"
  ssdc6[ "config" ] = { \
  "mon_a": "AudioDbfs", "mon_a_br": ssdc_scope['brightness'], "mon_a_cn": ssdc_scope['contrast'], "mon_a_xtra": "AudioChannel: 0", \
  "mon_b": "Histogram", "mon_b_br": ssdc_scope['brightness'], "mon_b_cn": ssdc_scope['contrast'] \
  }

  ssdc7 = {}
  ssdc7[ "name" ] = "ssdcfunc"
  ssdc7[ "caption" ] = "Off"
  ssdc7[ "config" ] = { "mon_a": "Picture", "mon_a_xtra": "Brightness: 0", "mon_b": "Picture", "mon_b_xtra": "Brightness: 0" }

  ssdcgrp = {}
  ssdcgrp[ "name" ] = "SmartScope Duo"
  ssdcgrp[ "actions" ] = ( ssdc1, ssdc2, ssdc3, ssdc4, ssdc5, ssdc6, ssdc7 )

  return( ssdcgrp, )


# Hook called when a custom action is triggered in the menu

def customUIAction( info, userData ):

  if( info['name'] == "ssdcfunc" ):

    # Connect to the SmartScope
    import socket

    tcpSocket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    try:
      tcpSocket.connect( (ssdc_hostname, 9992) )
    except socket.error:
      print( "smartscope-control.py: error connecting to " + ssdc_hostname + ":9992" )
      return

    tcpSocket.settimeout(1.0)

    # Sleep for a little bit to give the SmartScope time to dump its whole
    # preamble.  Yes, this is hacky, but I don't feel like writing a full-blown
    # input read/buffer system just for this
    time.sleep(0.2)

    # Receive all the preamble info the SmartScope sends us and throw it away
    # because we don't really care.. though maybe at some point we should
    try:
      tcpSocket.recv( 4096 )
    except socket.error:
      print( "smartscope-control.py: error reading from socket" )
      tcpSocket.close()
      return

    # Switch the displays
    if( 'mon_a' in userData['config'] ):
      tcpSocket.send( "MONITOR A:\n" if ssdc_swap is False else "MONITOR B:\n" )
      tcpSocket.send( "ScopeMode: " + userData['config']['mon_a'] + "\n" )
      if( 'mon_a_br' in userData['config'] ):
        tcpSocket.send( "Brightness: " + userData['config']['mon_a_br'] + "\n" )
      if( 'mon_a_cn' in userData['config'] ):
        tcpSocket.send( "Contrast: " + userData['config']['mon_a_cn'] + "\n" )
      if( 'mon_a_xtra' in userData['config'] ):
        tcpSocket.send( userData['config']['mon_a_xtra'] + "\n" )
      tcpSocket.send( "\n" )

    if( 'mon_b' in userData['config'] ):
      tcpSocket.send( "MONITOR B:\n" if ssdc_swap is False else "MONITOR A:\n" )
      tcpSocket.send( "ScopeMode: " + userData['config']['mon_b'] + "\n" )
      if( 'mon_b_br' in userData['config'] ):
        tcpSocket.send( "Brightness: " + userData['config']['mon_b_br'] + "\n" )
      if( 'mon_b_cn' in userData['config'] ):
        tcpSocket.send( "Contrast: " + userData['config']['mon_b_cn'] + "\n" )
      if( 'mon_b_xtra' in userData['config'] ):
        tcpSocket.send( userData['config']['mon_b_xtra'] + "\n" )
      tcpSocket.send( "\n" )

    time.sleep(0.2)
    tcpSocket.close()
