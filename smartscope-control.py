#!/bin/env python
# ******************************************************************************
#
# SmartScope Duo Controller for Flame v1.4
# Copyright (c) 2015-2022 Bob Maple (bobm-matchbox [at] idolum.com)
#
# Adds an entry to the Flame menu allowing control of the Blackmagic Design
# SmartScope Duo 4K - Updated for Flame 2022 (Python 3.7)


#### Configuration ####
ssdc_hostname = '192.168.1.1'  # IP or hostname of the SmartScope

# Separate Brightness and Contrast values for Scope displays vs Picture
# Ranges 0-255 with 127 being the default value (I use 75/180 for scope)
ssdc_scope    = { "brightness": "127", "contrast": "127" }
ssdc_picture  = { "brightness": "127", "contrast": "127" }

# Swaps the left and right monitors from how they appear in the menu
ssdc_swap     = False

#### End Configuration



def get_main_menu_custom_ui_actions():

  # Define our callback functions from Flame which just re-dispatch to
  # a single worker function that handles everything
  def smartscope_action_0(sel):
    smartscope_handler( { "mon_a": "Picture", "mon_a_br": "0", "mon_b": "Picture", "mon_b_br": "0" } )
  def smartscope_action_1(sel):
    smartscope_handler( { "mon_a": "ParadeRGB", "mon_b": "Vector75" } )
  def smartscope_action_2(sel):
    smartscope_handler( { "mon_a": "ParadeRGB", "mon_b": "Picture" } )
  def smartscope_action_3(sel):
    smartscope_handler( { "mon_a": "ParadeYUV", "mon_b": "Vector75" } )
  def smartscope_action_4(sel):
    smartscope_handler( { "mon_a": "ParadeYUV", "mon_b": "Picture" } )
  def smartscope_action_5(sel):
    smartscope_handler( { "mon_a": "WaveformLuma", "mon_b": "Picture" } )
  def smartscope_action_6(sel):
    smartscope_handler( { "mon_a": "AudioDbfs", "mon_a_xtra": "AudioChannel: 0", "mon_b": "Histogram" } )

  # Main worker function that talks to the SmartScope
  def smartscope_handler( userData ):
    import time, socket

    tcpSocket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    try:
      tcpSocket.connect( (ssdc_hostname, 9992) )
    except socket.error:
      print( "smartscope-control.py: error connecting to " + ssdc_hostname + ":9992" )
      return

    tcpSocket.settimeout(1.0)

    # Sleep for a little bit to give the SmartScope time to dump its
    # config on connect. Yes, this is hacky.
    time.sleep(0.2)

    # Receive all the config info the SmartScope sends us and throw it away
    # because we don't really care about it for our purposes
    try:
      tcpSocket.recv( 4096 )
    except socket.error:
      print( "smartscope-control.py: error reading from socket" )
      tcpSocket.close()
      return

    if( 'mon_a' in userData ):
      tmpstr  = "MONITOR A:\n" if ssdc_swap == False else "MONITOR B:\n"
      tmpstr += "ScopeMode: " + userData['mon_a'] + "\n"
      tcpSocket.send( tmpstr.encode( 'utf-8' ) )

      if( 'mon_a_br' in userData ):
      	tmpstr = "Brightness: " + userData['mon_a_br'] + "\n"
      else:
      	tmpstr = "Brightness: " + (ssdc_picture['brightness'] if userData['mon_a'] == "Picture" else ssdc_scope['brightness']) + "\n"

      tcpSocket.send( tmpstr.encode( 'utf-8' ) )

      if( 'mon_a_cn' in userData ):
        tmpstr = "Contrast: " + userData['mon_a_cn'] + "\n"
      else:
        tmpstr = "Contrast: " + (ssdc_picture['contrast'] if userData['mon_a'] == "Picture" else ssdc_scope['contrast']) + "\n"

      tcpSocket.send( tmpstr.encode( 'utf-8' ) )

      if( 'mon_a_xtra' in userData ):
        tmpstr = userData['mon_a_xtra'] + "\n"

      tmpstr += "\n"
      tcpSocket.send( tmpstr.encode( 'utf-8' ) )

    if( 'mon_b' in userData ):
      tmpstr  = "MONITOR B:\n" if ssdc_swap == False else "MONITOR A:\n"
      tmpstr += "ScopeMode: " + userData['mon_b'] + "\n"

      tcpSocket.send( tmpstr.encode( 'utf-8' ) )

      if( 'mon_b_br' in userData ):
        tmpstr = "Brightness: " + userData['mon_b_br'] + "\n"
      else:
        tmpstr = "Brightness: " + (ssdc_picture['brightness'] if userData['mon_b'] == "Picture" else ssdc_scope['brightness']) + "\n"

      tcpSocket.send( tmpstr.encode( 'utf-8' ) )

      if( 'mon_b_cn' in userData ):
        tmpstr = "Contrast: " + userData['mon_b_cn'] + "\n"
      else:
        tmpstr = "Contrast: " + (ssdc_picture['contrast'] if userData['mon_b'] == "Picture" else ssdc_scope['contrast']) + "\n"

      tcpSocket.send( tmpstr.encode( 'utf-8' ) )

      if( 'mon_b_xtra' in userData ):
        tmpstr = userData['mon_b_xtra'] + "\n"

      tmpstr += "\n"
      tcpSocket.send( tmpstr.encode( 'utf-8' ) )

    time.sleep(0.2)
    tcpSocket.close()

  # Return our custom menu which is inserted into the Flame menu
  return [
    {
      "name": "SmartScope Duo",
      "actions": [
        {
          "name": "Parade RGB | Vectorscope",
          "order": 1,
          "execute": smartscope_action_1
        },
        {
          "name": "Parade RGB | Picture",
          "order": 2,
          "execute": smartscope_action_2
        },
        {
          "name": "Parade YUV | Vectorscope",
          "order": 3,
          "execute": smartscope_action_3
        },
        {
          "name": "Parade YUV | Picture",
          "order": 4,
          "execute": smartscope_action_4
        },
        {
          "name": "Waveform | Picture",
          "order": 5,
          "execute": smartscope_action_5
        },
        {
          "name": "Audio Dbfs | Histogram",
          "order": 6,
          "execute": smartscope_action_6
        },
        {
          "name": "Off",
          "order": 7,
          "execute": smartscope_action_0
        }
      ]
    }
  ]
