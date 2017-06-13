//  _ ___ _______     ___ ___ ___  ___ _   _ ___ _____ ___ 
// / |_  )__ /   \   / __|_ _| _ \/ __| | | |_ _|_   _/ __| 
// | |/ / |_ \ |) | | (__ | ||   / (__| |_| || |  | | \__ \ 
// |_/___|___/___/   \___|___|_|_\\___|\___/|___| |_| |___/ 
// 
// The Unnamed Circuit
// 
// Made by sarutsel sarutsel
// License: CC-BY-SA 3.0
// Downloaded from: https://circuits.io/circuits/5201353-the-unnamed-circuit

//  _ ___ _______     ___ ___ ___  ___ _   _ ___ _____ ___ 
// / |_  )__ /   \   / __|_ _| _ \/ __| | | |_ _|_   _/ __| 
// | |/ / |_ \ |) | | (__ | ||   / (__| |_| || |  | | \__ \ 
// |_/___|___/___/   \___|___|_|_\\___|\___/|___| |_| |___/ 
// 
// ESP8266 Wifi Demo
// 
// Made by sarutsel sarutsel
// License: CC-BY-SA 3.0
// Downloaded from: https://circuits.io/circuits/5144160-esp8266-wifi-demo

int dist = A2;
double duration;
int distance;
double duration1;
int distance1;
bool fwd = true;
bool bwd = false;
float val, degreesC;

String ssid     = "Simulator Wifi";  // SSID to connect to
String password = ""; // Our virtual wifi has no password (so dont do your banking stuff on this network)

String host     = "pubsub.pubnub.com"; // Open Weather Map API
const int httpPort   = 80;

String g_pubKey     = "pub-c-52dfaf38-9202-447f-a5c4-4fffdd0fdeac";
String g_subKey     = "sub-c-09f86e3c-2e1e-11e7-97de-0619f8945a4f";
String g_channel    = "StatusChannel";
String timeToken    = "0";
String prevToken    = "0";

// the setup routine runs once when you press reset:
void setup() {
  
  // Start our ESP8266 Serial Communication
  Serial.begin(115200);   // Serial connection over USB to computer
  Serial.println("AT");   // Serial connection on Tx / Rx port to ESP8266
  delay(10);        // Wait a little for the ESP to respond
  if (!Serial.find("OK")) {}
    
  // Connect to 123D Circuits Simulator Wifi
  Serial.println("AT+CWJAP=\"" + ssid + "\",\"" + password + "\"");
  delay(10);        // Wait a little for the ESP to respond
  if (!Serial.find("OK")) {}
  
  // Open TCP connection to the host:
  Serial.println("AT+CIPSTART=\"TCP\",\"" + host + "\"," + httpPort);
  delay(50);        // Wait a little for the ESP to respond
  if (!Serial.find("OK")) {}
  
  String url = "/publish/pub-c-52dfaf38-9202-447f-a5c4-4fffdd0fdeac/sub-c-09f86e3c-2e1e-11e7-97de-0619f8945a4f/0/GetDevices/0/{\"Sensors\":{\"Room1\":{\"Temp\":\"Room1Temp\"}}}";
    Serial.println(url);

    String httpPacket = "GET " + url + " HTTP/1.1\r\nHost: " + host + "\r\n\r\n";
    int length = httpPacket.length();

    // Send our message length
    Serial.print("AT+CIPSEND=");
    Serial.println(length);
    delay(10); // Wait a little for the ESP to respond
    if (!Serial.find(">")) {}

    // Send our http request
    Serial.print(httpPacket);
    delay(10); // Wait a little for the ESP to respond
    if (!Serial.find("SEND OK\r\n")) {}

    while(!Serial.available()) delay(5);  // wait until we receive the response from the server

    if (Serial.find("\r\n\r\n")){ // search for a blank line which defines the end of the http header
      delay(5);

      unsigned int i = 0; //timeout counter
      String outputString = "";

    //while (!Serial.find("\"temp\":")){} // find the part we are interested in.

       // 1 minute timeout checker
        while(Serial.available()) {
          char c = Serial.read();
          if(c=='t') break; // break out of our loop because we got all we need
          outputString += c; // append to our output string
          i=0; // reset our timeout counter
        }
      prevToken = timeToken;
      timeToken=outputString.substring(outputString.length()-22,outputString.length()-3);
      String printstr = outputString.substring(1,outputString.length()-23);

    }

}
void beforeGet(){
  
}
// the loop routine runs over and over again forever:
void loop() {
  // Construct our HTTP call
  
  val = analogRead(A5) * 0.004882814;
  degreesC = (val - 0.5) * 100.0;
  Serial.println(degreesC);

  if(degreesC>25){
    String state = "\"True\"";
    if(fwd) state = "\"True\"";
    else if(bwd) state = "\"False\"";
    String url = "/publish/pub-c-52dfaf38-9202-447f-a5c4-4fffdd0fdeac/sub-c-09f86e3c-2e1e-11e7-97de-0619f8945a4f/0/Sensors/0/\"Room1\":\"AC\":\"True\"";
    Serial.println(url);

    String httpPacket = "GET " + url + " HTTP/1.1\r\nHost: " + host + "\r\n\r\n";
    int length = httpPacket.length();

    // Send our message length
    Serial.print("AT+CIPSEND=");
    Serial.println(length);
    delay(10); // Wait a little for the ESP to respond
    if (!Serial.find(">")) {}

    // Send our http request
    Serial.print(httpPacket);
    delay(10); // Wait a little for the ESP to respond
    if (!Serial.find("SEND OK\r\n")) {}

    while(!Serial.available()) delay(5);  // wait until we receive the response from the server

    if (Serial.find("\r\n\r\n")){ // search for a blank line which defines the end of the http header
      delay(5);

      unsigned int i = 0; //timeout counter
      String outputString = "";

    //while (!Serial.find("\"temp\":")){} // find the part we are interested in.

       // 1 minute timeout checker
        while(Serial.available()) {
          char c = Serial.read();
          if(c=='t') break; // break out of our loop because we got all we need
          outputString += c; // append to our output string
          i=0; // reset our timeout counter
        }
      prevToken = timeToken;
      timeToken=outputString.substring(outputString.length()-22,outputString.length()-3);
      String printstr = outputString.substring(1,outputString.length()-23);

    }

    delay(500); // wait 10 seconds before updating
  }
}
