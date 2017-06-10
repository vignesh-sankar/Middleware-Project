from pubnub import Pubnub
import json
import time
    
pubnub = Pubnub(publish_key = 'pub-c-52dfaf38-9202-447f-a5c4-4fffdd0fdeac', subscribe_key = 'sub-c-09f86e3c-2e1e-11e7-97de-0619f8945a4f')

DeviceStatus = False
DeviceName = {}
ControlDevice = {}

#Publish Channels
GetDeviceChannel = "GetDevices"
ControlChannel = "Sensors"

#Subscribe Channels
IndividualChannel = "Room1Motion"

room = "Room1"
device = "Motion"
cdevice = "Light1"

def Initialization():
	global DeviceName
	global ControlDevice
	global DeviceStatus
	global room
	global device
	global cdevice
	global ControlChannel
	global IndividualChannel
	DeviceName={"Sensors":{room:{device:IndividualChannel}}}
	ControlDevice={room:{cdevice:DeviceStatus}}
    
    #Give Intro
	pubnub.publish(channel = GetDeviceChannel, message = DeviceName)
	

Initialization()



