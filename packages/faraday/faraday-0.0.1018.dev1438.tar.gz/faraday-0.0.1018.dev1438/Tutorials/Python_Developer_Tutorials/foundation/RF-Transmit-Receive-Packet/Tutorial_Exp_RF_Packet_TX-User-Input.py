#!/usr/bin/env python

#Imports - General

import os
import sys

# Add Faraday library to the Python path.
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../..'))

# Imports - Faraday Specific
from faraday.proxyio import faradaybasicproxyio
from faraday.proxyio import faradaycommands


#Variables
local_device_callsign = 'REPLACEME'  # Should match the connected Faraday unit as assigned in Proxy configuration
local_device_node_id = 0  # Should match the connected Faraday unit as assigned in Proxy configuration

#Start the proxy server after configuring the configuration file correctly
#Setup a Faraday IO object
faraday_1 = faradaybasicproxyio.proxyio()
faraday_cmd = faradaycommands.faraday_commands()


##############
## TOGGLE Remote Device ++GPIO
##############

#Remote device information
remote_callsign = 'kb1lqd'
remote_id = 2

#NOTE: This TX program MUST operate on a different proxy TCP port than RX

#Use the predefined experimental message command (singled packet) function to send an RF message to a remote unit
#general_command.SendRfMsgExperimental('kb1lqd', 23, "Testing This Message 1!")

user_input = ''

while(user_input != "quit"):
    user_input = raw_input("Text To Transmit:")
    command = faraday_cmd.CommandLocalExperimentalRfPacketForward(remote_callsign, remote_id, str(user_input))
    print "Transmitting message:", user_input
    faraday_1.POST(local_device_callsign, local_device_node_id, faraday_1.CMD_UART_PORT, command)

##message = "Testing RF Packet 1"
##command = faraday_cmd.CommandLocalExperimentalRfPacketForward(remote_callsign, remote_id, message)
##print "Transmitting message:", message
##faraday_1.POST(local_device_callsign, local_device_node_id, faraday_1.CMD_UART_PORT, command)
##
##message = "Testing RF Packet 2"
##command = faraday_cmd.CommandLocalExperimentalRfPacketForward(remote_callsign, remote_id, message)
##print "Transmitting message:", message
##faraday_1.POST(local_device_callsign, local_device_node_id, faraday_1.CMD_UART_PORT, command)
###Uncomment to send multiple concecutive messages!
##general_command.SendRfMsgExperimental('kb1lqd', 23, "Testing This Message 2!")
##general_command.SendRfMsgExperimental('kb1lqd', 23, "Testing This Message 3!")
##general_command.SendRfMsgExperimental('kb1lqd', 23, "Testing This Message 4!")
##general_command.SendRfMsgExperimental('kb1lqd', 23, "Testing This Message 5!")
