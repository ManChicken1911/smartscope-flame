#!/bin/env python
# ******************************************************************************
#
# SmartScope Duo Controller for Flame v1.0
# Copyright (c) 2015 Bob Maple (bobm-matchbox [at] idolum.com)
#
# Adds a context menu to switch the monitors of the Blackmagic Design
# SmartScope Duo 4K


#### Configuration ####
ssdc_hostname = '192.168.1.1'  # IP or hostname
####


# Build the context menu and return it to Flame
#
# mon_a is the left display, mon_b is the right display
# The possible modes for each display can be found in the
# SmartScope Manual in the Developer Information section.

def getCustomUIActions( ):

  ssdc1 = {}
  ssdc1[ "name" ] = "ssdcfunc"
  ssdc1[ "caption" ] = "Parade RGB | Vectorscope"
  ssdc1[ "config" ] = { "mon_a": "ParadeRGB", "mon_b": "Vector75" }

  ssdc2 = {}
  ssdc2[ "name" ] = "ssdcfunc"
  ssdc2[ "caption" ] = "Parade RGB | Picture"
  ssdc2[ "config" ] = { "mon_a": "ParadeRGB", "mon_b": "Picture" }

  ssdc3 = {}
  ssdc3[ "name" ] = "ssdcfunc"
  ssdc3[ "caption" ] = "Parade YUV | Vectorscope"
  ssdc3[ "config" ] = { "mon_a": "ParadeYUV", "mon_b": "Vector75" }

  ssdc4 = {}
  ssdc4[ "name" ] = "ssdcfunc"
  ssdc4[ "caption" ] = "Parade YUV | Picture"
  ssdc4[ "config" ] = { "mon_a": "ParadeYUV", "mon_b": "Picture" }

  ssdc5 = {}
  ssdc5[ "name" ] = "ssdcfunc"
  ssdc5[ "caption" ] = "Audio Dbfs | Histogram"
  ssdc5[ "config" ] = { "mon_a": "AudioDbfs", "mon_a_xtra": "AudioChannel: 0", "mon_b": "Histogram" }

  ssdcgrp = {}
  ssdcgrp[ "name" ] = "SmartScope Duo"
  ssdcgrp[ "actions" ] = ( ssdc1, ssdc2, ssdc3, ssdc4, ssdc5 )

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

    tcpSocket.setblocking(0)
    tcpSocket.settimeout(3)

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
      tcpSocket.send( "MONITOR A:\n" )
      tcpSocket.send( "ScopeMode: " + userData['config']['mon_a'] + "\n" )
      if( 'mon_a_xtra' in userData['config'] ):
        tcpSocket.send( userData['config']['mon_a_xtra'] + "\n" )
      tcpSocket.send( "\n" )

    if( 'mon_b' in userData['config'] ):
      tcpSocket.send( "MONITOR B:\n" )
      tcpSocket.send( "ScopeMode: " + userData['config']['mon_b'] + "\n" )
      if( 'mon_b_xtra' in userData['config'] ):
        tcpSocket.send( userData['config']['mon_b_xtra'] + "\n" )
      tcpSocket.send( "\n" )

    tcpSocket.close()
