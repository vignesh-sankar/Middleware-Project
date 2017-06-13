/*********************************************************************************
  Pubnub Subscribe Sample
*********************************************************************************/
#include <ArduinoJson.h>
#include <ESP8266WiFi.h>

const char* g_ssid       = "AndroidAP";
const char* g_password   = "natarajan";
const char* g_host       = "pubsub.pubnub.com";
const char* g_pubKey     = "pub-c-52dfaf38-9202-447f-a5c4-4fffdd0fdeac";
const char* g_subKey     = "sub-c-09f86e3c-2e1e-11e7-97de-0619f8945a4f";
const char* g_channel    = "Room2Light2";
String      timeToken    = "0";
String      msg          = "";
bool        state        = false;
String      url          = "";
int sensorPin = A0; // select the input pin for LDR
int sensorValue = 0; // variable to store the value coming from the sensor


typedef enum RET{
  FAILURE = 0,
  SUCCESS
}RET_VALUE;
/*********************************************************************************
  Function Name     : setup
  Description       : Initialize the Serial Communication with baud 115200, Begin
                    the ESP8266 and connect to the Router and print the ip
  Parameters        : void
  Return            : void
*********************************************************************************/

void setup()
{
  Serial.begin(115200);
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(g_ssid);

  WiFi.begin(g_ssid, g_password);

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  pinMode(D0, OUTPUT);

}

/*********************************************************************************
  Function Name     : loop
  Description       : Connect to the PUBNUB REST API with TCP/IP Connection
                    and Subscribe the sample data from the pubnub
  Parameters        : void
  Return            : void
*********************************************************************************/

void loop()
{
  WiFiClient client;
  const int l_httpPort = 80;
  if (!client.connect(g_host, l_httpPort))
  {
    Serial.println("connection failed");
    return;
  }
  //DATA FORMAT : http://pubsub.pubnub.com/publish/pub-key/sub-key/signature/channel/callback/message
  //SUB FORMAT :  http://pubsub.pubnub.com/subscribe/sub-key/channel/callback/timetoken
  if(msg.equals("Status")){
    url = "/publish/";
      url += g_pubKey;
      url += "/";
      url += g_subKey;
      url += "/0/RetrieveStatus";
      url += "/0/";
      url += "{\"Actuators\":{\"Room1\":{\"Light1\":{\"Status\":"+ String(state) +",\"Channel:\":\"Room2Light2\"}}}}";
      
  }
  else{
    url = "/subscribe/";
  url += g_subKey;
  url += "/";
  url += g_channel;
  url += "/0/";
  url += timeToken;
  //Serial.println(url);  
  }
  
  Serial.println(url);
  client.print(String("GET ") + url + " HTTP/1.1\r\n" +
               "Host: " + g_host + "\r\n" +
               "Connection: close\r\n\r\n");
  delay(50);

  while (client.available())
  {
    String line = client.readStringUntil('\r');
    timeToken=line.substring(line.length()-19,line.length()-2);
    msg = line.substring(4, line.length()-23);
    Serial.println(msg);
    if(msg.equals("Status")){
      Serial.println(state);
      
//    
//      client.print(String("GET ") + url + " HTTP/1.1\r\n" +
//                   "Host: " + g_host + "\r\n" +
//                   "Connection: close\r\n\r\n");
//      delay(50);
    
//      while (client.available())
//      {
//        String line = client.readStringUntil('\r');
//        Serial.println(line);
//        delay(50);
//      }
    }
    else if(msg.indexOf("app")>0){ 
      if(msg.indexOf("True")>=0){
        state=true;
        digitalWrite(D0, HIGH);
        Serial.println("True in app detected");
      }
      
      else{
        state=false;
        digitalWrite(D0, LOW);
        Serial.println("False in app detected");
      }
    }
    else if(msg.indexOf("sen")>0){
      if(msg.indexOf("True")>=0){
        sensorValue = analogRead(sensorPin); // read the value from the sensor
        Serial.println(sensorValue);
        if(sensorValue>100) break;
        state = true;
        digitalWrite(D0, HIGH);
        Serial.println("True in sensor detected");
      }
      
      else{
        state= false;
        digitalWrite(D0, LOW);
        Serial.println("False in sensor detected");
      }
    }
  }
  //Serial.println("closing connection");
  delay(1000);
}
