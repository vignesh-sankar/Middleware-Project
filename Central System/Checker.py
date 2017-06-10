from pubnub import Pubnub
import json
import time

pubnub = Pubnub(publish_key = 'pub-c-52dfaf38-9202-447f-a5c4-4fffdd0fdeac', subscribe_key = 'sub-c-09f86e3c-2e1e-11e7-97de-0619f8945a4f')

#Initialize 
NoOfMsgs = 0
NoOfDevices = 0
start_time = time.time()

#Subscribe Channels
StatusChannel      = "StatusReport"

#Publish Channels
StatusReportChannel  = "Checker"


def GetStatusCallback(message, channel):
    time.sleep(4)
    pubnub.publish(channel = StatusReportChannel, message = "Check")

pubnub.subscribe( StatusChannel,      callback = GetStatusCallback )
