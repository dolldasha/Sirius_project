#include <Ethernet.h>
#include <SPI.h>

// socket server address
IPAddress server(192, 168, 1, 72);
#define port 8887

IPAddress ip(192, 168, 1, 177);
IPAddress myDns(192, 168, 0, 1);

#define id "125ffa23"

byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };

EthernetClient client;

const int analog_sensor_signal = A1;
const int digital_sensor_signal = 8;

int value = 0;

void get_data_from_sensor(){
  value = analogRead(analog_sensor_signal);
  int temp = digitalRead(digital_sensor_signal);
  Serial.print(temp);
  Serial.print(' ');
  Serial.println(value);
}

void send_data(){
  if (client.connect(server, 8887)) {
    Serial.print("connected to ");
    Serial.println(client.remoteIP());
    // Make a HTTP request:
    //String data = id + ':' + value;
    Serial.print("Sending data: ");
    Serial.print(id);
    Serial.print(":");
    Serial.println(value);
    String data = id;
    data += ':';
    data += String(value);
    client.println(data);
  } else {
    // if you didn't get a connection to the server:
    Serial.println("connection failed");
  }
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(digital_sensor_signal, INPUT);
  pinMode(analog_sensor_signal, INPUT);
  Serial.println("Initialize Ethernet with DHCP:");
  Ethernet.begin(mac, ip, myDns);
  if (false) {
    Serial.println("Failed to configure Ethernet using DHCP");
    // Check for Ethernet hardware present
    if (Ethernet.hardwareStatus() == EthernetNoHardware) {
      Serial.println("Ethernet shield was not found.  Sorry, can't run without hardware. :(");
      while (true) {
        delay(1); // do nothing, no point running without Ethernet hardware
      }
    }
    if (Ethernet.linkStatus() == LinkOFF) {
      Serial.println("Ethernet cable is not connected.");
    }
    // try to congifure using IP address instead of DHCP:
    Ethernet.begin(mac, ip, myDns);
  } else {
    Serial.print("  DHCP assigned IP ");
    Serial.println(Ethernet.localIP());
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  delay(1000);
  get_data_from_sensor();
  send_data();
}
