#include <ESP8266WiFi.h>
#include <MySQL_Connection.h>
#include <MySQL_Cursor.h>

IPAddress server_addr(10,0,1,35);  // IP of the MySQL *server* here
char user[] = "cisc340admin";              // MySQL user login username
char password[] = "!Xadmin2018";        // MySQL user login password
char ssid[] = "cisc340";
char pass[] = "Hut!2&FR0";
String data;

// Sample query
String INSERT_PART = "INSERT INTO lifebright.data (timestamp, heartrate, temp, motion_x, motion_y, motion_z) VALUES (";
//char INSERT_SQL[] = "INSERT INTO test_arduino.hello_arduino (message) VALUES ('Hello, Arduino!')";

WiFiClient client;                 // Use this for WiFi instead of EthernetClient
MySQL_Connection conn(&client);
MySQL_Cursor* cursor;

void setup()
{
  Serial.begin(115200);
  // Begin WiFi section
  Serial.printf("\nConnecting to %s", ssid);
  WiFi.begin(ssid, pass);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to network");
  Serial.print("My IP address is: ");
  Serial.println(WiFi.localIP());

  Serial.print("Connecting to SQL...  ");
  if (conn.connect(server_addr, 1433, user, password))
    Serial.println("OK.");
  else
    Serial.println("FAILED.");
  cursor = new MySQL_Cursor(&conn);
}

void loop()
{
//  if (conn.connected()) {
//    while (Serial.available() > 0) {
//      data += char(Serial.read());
//      delay(1);
//    }
//    data = INSERT_PART + data;
//    cursor->execute(data.c_str());
//    delay(2);
//    data = ""
//  }
//  delay(5000);

  while (Serial.available() > 0) {
    data += char(Serial.read());
    delay(1);
  }
  data = INSERT_PART + data;
  Serial.println(data.c_str());
  delay(2);
  data = "";
  delay(5000);
}
