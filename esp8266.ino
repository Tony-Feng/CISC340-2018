// #include <ESP8266WiFi.h>
// #include <MySQL_Connection.h>
// #include <MySQL_Cursor.h>

// IPAddress server_addr(10,0,1,35);  // IP of the MySQL *server* here
// char user[] = "cisc340admin";              // MySQL user login username
// char password[] = "!Xadmin2018";        // MySQL user login password
// char ssid[] = "cisc340";
// char pass[] = "Hut!2&FR0";
// String data;

// // Sample query
// String INSERT_PART = "INSERT INTO lifebright.data (timestamp, heartrate, temp, motion_x, motion_y, motion_z) VALUES (";
// //char INSERT_SQL[] = "INSERT INTO test_arduino.hello_arduino (message) VALUES ('Hello, Arduino!')";

// WiFiClient client;                 // Use this for WiFi instead of EthernetClient
// MySQL_Connection conn(&client);
// MySQL_Cursor* cursor;

// void setup()
// {
//   Serial.begin(115200);
//   // Begin WiFi section
//   Serial.printf("\nConnecting to %s", ssid);
//   WiFi.begin(ssid, pass);
//   while (WiFi.status() != WL_CONNECTED) {
//     delay(500);
//     Serial.print(".");
//   }
//   Serial.println("\nConnected to network");
//   Serial.print("My IP address is: ");
//   Serial.println(WiFi.localIP());

//   Serial.print("Connecting to SQL...  ");
//   if (conn.connect(server_addr, 1433, user, password))
//     Serial.println("OK.");
//   else
//     Serial.println("FAILED.");
//   cursor = new MySQL_Cursor(&conn);
// }

// void loop()
// {
// //  if (conn.connected()) {
// //    while (Serial.available() > 0) {
// //      data += char(Serial.read());
// //      delay(1);
// //    }
// //    data = INSERT_PART + data;
// //    cursor->execute(data.c_str());
// //    delay(2);
// //    data = ""
// //  }
// //  delay(5000);

//   while (Serial.available() > 0) {
//     data += char(Serial.read());
//     delay(1);
//   }
//   data = INSERT_PART + data;
//   Serial.println(data.c_str());
//   delay(2);
//   data = "";
//   delay(5000);
// }















// #include <ESP8266HTTPClient.h>
// #include <ESP8266WiFi.h>

// String data;

// void setup() {
//   Serial.begin(115200);                 //Serial connection
//   WiFi.begin("cisc340", "Hut!2&FR0");   //WiFi connection
//   while (WiFi.status() != WL_CONNECTED) {  //Wait for the WiFI connection completion
//     delay(500);
//     Serial.println(".");
//   }
// }

// void loop() {
//   if(WiFi.status()== WL_CONNECTED){   //Check WiFi connection status
//     while (Serial.available() > 0) {
//       data += char(Serial.read());
//       delay(1);
//     }
//     if(data.length() > 0){
//       HTTPClient http;    //Declare object of class HTTPClient
      
//       http.begin("http://40.85.246.118:8080/store");      //Specify request destination
//       http.addHeader("Content-Type", "application/json");  //Specify content-type header
      
//       int httpCode = http.POST(data);   //Send the request
//       String payload = http.getString();                  //Get the response payload
//       Serial.println(httpCode);   //Print HTTP return code
//       Serial.println(payload);    //Print request response payload
//       http.end();  //Close connection
//       data = "";
//     }
//   }else{
//     Serial.println("Error in WiFi connection");
//   }
//   delay(3000);  //Send a request every 30 seconds
// }




































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
