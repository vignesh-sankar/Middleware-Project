from pubnub import Pubnub
import json
import time

pubnub = Pubnub(publish_key = 'pub-c-52dfaf38-9202-447f-a5c4-4fffdd0fdeac', subscribe_key = 'sub-c-09f86e3c-2e1e-11e7-97de-0619f8945a4f')

#Initialize 
NoOfMsgs = 0
NoOfDevices = 0
start_time = time.time()

#Subscribe Channels
GetDeviceChannel      = "GetDevices"
GetStatusChannel      = "GetStatus"
StatusRetrieveChannel = "RetrieveStatus"
ControlChannel        = "Control"
SensorChannel         = "Sensors"
DeviceReplyChannel    = "DevReply

#Publish Channels
StatusReportChannel  = "StatusReport"
statusSendChannel    = "StatusChannel"
DeviceControlChannel = "DeviceControl"

#Store the devices connected.
DevicesIntact={"House":{ }};

# Call back for initial device registration
def GetDeviceCallback(message, channel):
    global NoOfDevices
    
    jsonObject = json.loads(json.dumps(message));
    NewDeviceIntact = json.dumps(DevicesIntact);

    for name in jsonObject:
        print(name)
        for devType in jsonObject[name]:
            print(devType)
            for device in jsonObject[name][devType]:
                print(device)
                if(DevicesIntact['House'].get(name)):
                    if(DevicesIntact['House'][name].get(devType)):
                        if((DevicesIntact['House'][name][devType].get(device))):
                            print("Already exist")
                        else:
                            DevicesIntact['House'][name][devType][device]=(jsonObject[name][devType][device])
                            print(DevicesIntact)
                            if(name == "Actuators"):
                                NoOfDevices+=1
                    else:
                        DevicesIntact['House'][name][devType]=(jsonObject[name][devType]);
                        print(DevicesIntact)
                        if(name == "Actuators"):
                            NoOfDevices+=1
                else:
                    DevicesIntact['House'][name]=(jsonObject[name]);
                    print(DevicesIntact)
                    if(name == "Actuators"):
                        NoOfDevices+=1
    #DevicesIntact = NewDeviceIntact;

# Call back for handling status query from various devices
def GetStatusCallback(message, channel):
    print('['+channel+']: '+json.dumps(message))
    jsonObject = json.loads(json.dumps(message))
    #DevicesIntact['Houses']=message;
    global NoOfMsgs
    global start_time
    if NoOfMsgs>0 and NoOfMsgs<NoOfDevices:
        print("Already asked")
    else:
        NoOfMsgs =0
        start_time = time.time()
        pubnub.publish(channel = StatusReportChannel, message = message)
    # pubnub.publish(channel = StatusRetrieveChannel, message = json.dumps(DevicesIntact))

# Call back for sending the retrieved status from each device
def StatusRetrieve(message, channel):
    global NoOfMsgs
    NoOfMsgs+=1
    jsonObject = json.loads(json.dumps(message))
    print(jsonObject)
    for x in jsonObject:
        for i in jsonObject[x]:
            for j in jsonObject[x][i]:
                DevicesIntact['House'][x][i][j]['Status']=jsonObject[x][i][j]
    # print('['+channel+']: '+DevicesIntact+' N:'+str(NoOfMsgs))
    if(NoOfMsgs == NoOfDevices):
        pubnub.publish(channel = statusSendChannel, message = DevicesIntact['House']['Actuators'])

# Call back for sending control signal to the actuators
def ControlCallback(message, channel):
    print('['+channel+']:'+ str(message))
    jsonObject = json.loads(json.dumps(message))
    for name in jsonObject:
	print(name)
	if(DevicesIntact['House']['Actuators'].get(name)):
	    for devType in jsonObject[name]:
		print(devType)
		if(DevicesIntact['House']['Actuators'][name].get(devType)):
		    DevicesIntact['House']['Actuators'][name][devType]['Status']=jsonObject[name][devType]
		    pubnub.publish(channel = DevicesIntact['House']['Actuators'][name][devType]['Channel'], message = jsonObject[name][devType]+":app")
    print(DevicesIntact)
	
# Call back for sending control signal to actuators from sensors
def SensorCallback(message, channel):
    print('['+channel+']:'+ str(message))
    jsonObject = json.loads(json.dumps(message))
    for name in jsonObject:
	print(name)
	if(DevicesIntact['House']['Actuators'].get(name)):
	    for devType in jsonObject[name]:
		print(devType)
		if(DevicesIntact['House']['Actuators'][name].get(devType)):
		    DevicesIntact['House']['Actuators'][name][devType]['Status']=jsonObject[name][devType]
		    pubnub.publish(channel = DevicesIntact['House']['Actuators'][name][devType]['Channel'], message = jsonObject[name][devType]+":sen")
    print(DevicesIntact)

# Call back for retrieving status from the device that was controlled
def DeviceReply(message, channel):
    print('['+channel+']:'+ str(message))
    for name in jsonObject:
	print(name)
	if(DevicesIntact['House']['Actuators'].get(name)):
	    for devType in jsonObject[name]:
		print(devType)
		if(DevicesIntact['House']['Actuators'][name].get(devType)):
		    DevicesIntact['House']['Actuators'][name][devType]['Status']=jsonObject[name][devType]
    

pubnub.subscribe( GetDeviceChannel,      callback = GetDeviceCallback )
pubnub.subscribe( GetStatusChannel,      callback = GetStatusCallback )
pubnub.subscribe( StatusRetrieveChannel, callback = StatusRetrieve    )
pubnub.subscribe( ControlChannel,        callback = ControlCallback   )
pubnub.subscribe( SensorChannel,         callback = SensorCallback    )
pubnub.subscribe( DeviceReplyChannel,    callback = DeviceReply       )
