from pubnub import Pubnub
import mysql.connector
import json
import time

pubnub = Pubnub(publish_key = 'pub-c-52dfaf38-9202-447f-a5c4-4fffdd0fdeac', subscribe_key = 'sub-c-09f86e3c-2e1e-11e7-97de-0619f8945a4f')

#Initialize 
NoOfMsgs = 0
NoOfDevices = 0
done = 0
start_time = time.time()

#Subscribe Channels
GetDeviceChannel      = "GetDevices"
GetStatusChannel      = "GetStatus"
StatusRetrieveChannel = "RetrieveStatus"
ControlChannel        = "Control"
SensorChannel         = "Sensors"
DeviceReplyChannel    = "DevReply"
CheckerChannel        = "Checker"
GasSensor             = "GasSensor"

#Publish Channels
StatusReportChannel  = "StatusReport"
statusSendChannel    = "StatusChannel"
DeviceControlChannel = "DeviceControl"

#Store the devices connected.
DevicesIntact={"House":{ }};
DevicesResponse = {"Resp":{}};

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
                concatStr = devType+"|"+device
                if(DevicesIntact['House'].get(name)):
                    if(DevicesIntact['House'][name].get(devType)):
                        if((DevicesIntact['House'][name][devType].get(device))):
                            print("Already exist")
                        else:
                            DevicesIntact['House'][name][devType][device]=(jsonObject[name][devType][device])
                            print(DevicesIntact)
                            if(name == "Actuators"):
                                NoOfDevices+=1
                                DevicesResponse['Resp'][concatStr]=False
                    else:
                        DevicesIntact['House'][name][devType]=(jsonObject[name][devType]);
                        print(DevicesIntact)
                        if(name == "Actuators"):
                            NoOfDevices+=1
                            DevicesResponse['Resp'][concatStr]=False
                else:
                    DevicesIntact['House'][name]=(jsonObject[name])
                    print(DevicesIntact)
                    if(name == "Actuators"):
                        NoOfDevices+=1
                        DevicesResponse['Resp'][concatStr]=False
    print(DevicesResponse)
    #DevicesIntact = NewDeviceIntact;

# Call back for handling status query from various devices
def GetStatusCallback(message, channel):
    print('['+channel+']: '+json.dumps(message))
    jsonObject = json.loads(json.dumps(message))
    #DevicesIntact['Houses']=message;
    global NoOfMsgs
    global start_time
    global DeviceResponse
    global done
    if NoOfMsgs>0 and NoOfMsgs<NoOfDevices:
        print("Already asked")
    else:
        NoOfMsgs =0
        done = 0
        print(done)
        pubnub.publish(channel = StatusReportChannel, message = message)
    # pubnub.publish(channel = StatusRetrieveChannel, message = json.dumps(DevicesIntact))

def CheckerCallback(message, channel):
    global NoOfMsgs
    global done
    global DevicesResponse
    
    print("Checker")
    print(done)
    print(NoOfMsgs)
    if NoOfMsgs == 0 and done == 0:
        pubnub.publish(channel = statusSendChannel, message = "NDD")
        print("NDD")
        NoOfMsgs =0
    elif NoOfMsgs < NoOfDevices and done == 0:
        for num in DevicesResponse['Resp']:
            if(DevicesResponse['Resp'][num]== False):
                split = num.split("|")
                DevicesIntact['House']['Actuators'][split[0]][split[1]]['Status']="Failure"
            else:
                DevicesResponse['Resp'][num]= False
        print(DevicesIntact['House']['Actuators'])
        pubnub.publish(channel = statusSendChannel, message = DevicesIntact['House']['Actuators'])
        NoOfMsgs=0
        
# Call back for sending the retrieved status from each device
def StatusRetrieve(message, channel):
    global NoOfMsgs
    global done
    global DevicesResponse
                    
    NoOfMsgs+=1
    jsonObject = json.loads(json.dumps(message))
    print(jsonObject)
    for x in jsonObject:
        for i in jsonObject[x]:
            for j in jsonObject[x][i]:
                DevicesIntact['House'][x][i][j]['Status']=jsonObject[x][i][j]
                DevicesResponse['Resp'][i+"|"+j]=True
    # print('['+channel+']: '+DevicesIntact+' N:'+str(NoOfMsgs))
    if(NoOfMsgs == NoOfDevices):
        pubnub.publish(channel = statusSendChannel, message = DevicesIntact['House']['Actuators'])
        NoOfMsgs=0
        for num in DevicesResponse['Resp']:
            DevicesResponse['Resp'][num]= False
        done=1

# Call back for sending control signal to the actuators
def ControlCallback(message, channel):
    print('['+channel+']:'+ str(message))
    splits=message.split(":");
    #jsonObject = json.loads(json.dumps(message))
    if(DevicesIntact['House']['Actuators'].get(splits[0])):
        if(DevicesIntact['House']['Actuators'][splits[0]].get(splits[1])):
            if(splits[2] == "false"):
                DevicesIntact['House']['Actuators'][splits[0]][splits[1]]['Status']=False
            else:
                DevicesIntact['House']['Actuators'][splits[0]][splits[1]]['Status']=True
	    pubnub.publish(channel = DevicesIntact['House']['Actuators'][splits[0]][splits[1]]['Channel'], message = splits[2]+":app")

    pubnub.publish(channel = statusSendChannel, message = DevicesIntact['House']['Actuators'])
    print(DevicesIntact)
	
# Call back for sending control signal to actuators from sensors
def SensorCallback(message, channel):
    print('['+channel+']:'+ str(message))
    splits=message.split(":");
    #jsonObject = json.loads(json.dumps(message))
    if(DevicesIntact['House']['Actuators'].get(splits[0])):
        if(DevicesIntact['House']['Actuators'][splits[0]].get(splits[1])):
            DevicesIntact['House']['Actuators'][splits[0]][splits[1]]['Status']=splits[2]
	    pubnub.publish(channel = "GetStatus", message = DevicesIntact['House']['Actuators'])
	    pubnub.publish(channel = DevicesIntact['House']['Actuators'][name][devType]['Channel'], message = splits[2]+":sen")
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
    

def GasCallback(message, channel):
    cnx = mysql.connector.connect(user='user', password='vidhya567',
                              host='localhost',
                              database='Middleware')

    cursor = cnx.cursor()

    query = ("SELECT * FROM LoginDetails")

    cursor.execute(query)
    print(cursor)
    for (name) in cursor:
        print("{}".format(name))

    cursor.close()
    cnx.close()


pubnub.subscribe( GetDeviceChannel,      callback = GetDeviceCallback )
pubnub.subscribe( GetStatusChannel,      callback = GetStatusCallback )
pubnub.subscribe( StatusRetrieveChannel, callback = StatusRetrieve    )
pubnub.subscribe( ControlChannel,        callback = ControlCallback   )
pubnub.subscribe( SensorChannel,         callback = SensorCallback    )
pubnub.subscribe( DeviceReplyChannel,    callback = DeviceReply       )
pubnub.subscribe( CheckerChannel,        callback = CheckerCallback   )
pubnub.subscribe( GasSensor,             callback = GasCallback       )
