#include <ESP8266HTTPClient.h>
#include <ESP8266WiFi.h>

char ssid[] = "cisc340";
char pass[] = "Hut!2&FR0";
String data;

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, pass);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
}

//{"timestamp:946699947,"heartrate":0,"temp":-20,"motion_x":9,"motion_y":19,"motion_z":29}
//{"motion_x": 0.0, "timestamp": 946684817, "motion_y": -0.114914, "heartrate": 0, "motion_z": 9.15482, "temp": 23}
void loop() {
  if(WiFi.status() == WL_CONNECTED){   //Check WiFi connection status
    while (Serial.available() > 0) {
      data += char(Serial.read());
      delay(1);
    }
    if(data.length() > 0){
      HTTPClient http;    //Declare object of class HTTPClient
      
      http.begin("http://cisc340.canadacentral.cloudapp.azure.com:8080/store");      //Specify request destination
      http.addHeader("Content-Type", "application/json");  //Specify content-type header
      
      int httpCode = http.POST(data);   //Send the request
      String payload = http.getString(); //Get the response payload
      
      http.end();  //Close connection
      data = "";
    }
  }
  delay(1000);  //Send a request every 1 seconds
}
