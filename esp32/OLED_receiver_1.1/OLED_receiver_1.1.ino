/*
 * Ensure TTGO LORA32-OLED V1 board selected
 * Process goes:
 * - capture data
 * - forward to api
 * - disply onsite data on OLED for Rob
 * - display time since last message
 */

//watchdog lib
#include "esp_system.h"
#include <Wire.h>  // Only needed for Arduino 1.6.5 and earlier
//needs this lib https://github.com/ThingPulse/esp8266-oled-ssd1306 (daniel somethig in libs for arduino)
#include "SSD1306.h"

#include <SPI.h>
#include <LoRa.h>
#include <WiFi.h>
//#include <WiFi101.h>
//don't use arduin http client, use this: https://github.com/espressif/arduino-esp32/blob/51a4432ca8e71be202358ceb068f3047bb8ad762/libraries/HTTPClient/src/HTTPClient.h
// with instructions: https://techtutorialsx.com/2017/05/19/esp32-http-get-requests/
#include <HTTPClient.h>
#include "secrets.h"
#include <ArduinoJson.h> //using version 5

/* secrets.h format
 *  #define MYSSID ""
 *  #define PASS ""
 *  #define SENSOR_NAME ""  //location of sensor node (eg "lounge"
 *  #define SITE ""  //Site of sensor net install
 *  String API_user = "";
 *  String API_pass = "";
 *  #define SERVER_443_data "https://<url of api endpoint for data ingress>"
 *  #define SERVER_443_auth "https://<auth route>"
 */

// (something, SDA, SCL), see
//https://github.com/LilyGO/TTGO-LORA32-V2.0/issues/3
SSD1306 display(0x3c, 21, 22);

#define SS 18
#define RST 23
#define DI0 26

// LoRa Settings (these a lib defaults)
#define BAND 433E6
#define spreadingFactor 7
#define SignalBandwidth 125E3

#define codingRateDenominator 8

//variables
unsigned long new_rec;
unsigned long old_rec;
unsigned long start_time;
int mins;
int hours;
int secs;
int minutes;
int seconds;
const unsigned long COUNT_THRESH = 2000;
unsigned long timestamp;
int count;
const char sensorID[] = SENSOR_NAME;
String Token;
String time_disp;
String data;

///////please enter your sensitive data in the Secret tab/secrets.h
/////// Wifi Settings ///////
const char* ssid = MYSSID;
const char* password = PASS;

// CA details for https:
// https://techtutorialsx.com/2017/11/18/esp32-arduino-https-get-request/
const char* root_ca= \
"-----BEGIN CERTIFICATE-----\n" \
"MIIDSjCCAjKgAwIBAgIQRK+wgNajJ7qJMDmGLvhAazANBgkqhkiG9w0BAQUFADA/\n" \
"MSQwIgYDVQQKExtEaWdpdGFsIFNpZ25hdHVyZSBUcnVzdCBDby4xFzAVBgNVBAMT\n" \
"DkRTVCBSb290IENBIFgzMB4XDTAwMDkzMDIxMTIxOVoXDTIxMDkzMDE0MDExNVow\n" \
"PzEkMCIGA1UEChMbRGlnaXRhbCBTaWduYXR1cmUgVHJ1c3QgQ28uMRcwFQYDVQQD\n" \
"Ew5EU1QgUm9vdCBDQSBYMzCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEB\n" \
"AN+v6ZdQCINXtMxiZfaQguzH0yxrMMpb7NnDfcdAwRgUi+DoM3ZJKuM/IUmTrE4O\n" \
"rz5Iy2Xu/NMhD2XSKtkyj4zl93ewEnu1lcCJo6m67XMuegwGMoOifooUMM0RoOEq\n" \
"OLl5CjH9UL2AZd+3UWODyOKIYepLYYHsUmu5ouJLGiifSKOeDNoJjj4XLh7dIN9b\n" \
"xiqKqy69cK3FCxolkHRyxXtqqzTWMIn/5WgTe1QLyNau7Fqckh49ZLOMxt+/yUFw\n" \
"7BZy1SbsOFU5Q9D8/RhcQPGX69Wam40dutolucbY38EVAjqr2m7xPi71XAicPNaD\n" \
"aeQQmxkqtilX4+U9m5/wAl0CAwEAAaNCMEAwDwYDVR0TAQH/BAUwAwEB/zAOBgNV\n" \
"HQ8BAf8EBAMCAQYwHQYDVR0OBBYEFMSnsaR7LHH62+FLkHX/xBVghYkQMA0GCSqG\n" \
"SIb3DQEBBQUAA4IBAQCjGiybFwBcqR7uKGY3Or+Dxz9LwwmglSBd49lZRNI+DT69\n" \
"ikugdB/OEIKcdBodfpga3csTS7MgROSR6cz8faXbauX+5v3gTt23ADq1cEmv8uXr\n" \
"AvHRAosZy5Q6XkjEGB5YGV8eAlrwDPGxrancWYaLbumR9YbK+rlmM6pZW87ipxZz\n" \
"R8srzJmwN0jP41ZL9c8PDHIyh8bwRLtTcm1D9SZImlJnt1ir/md2cXjbDaJWFBM5\n" \
"JDGFoqgCWjBH4d1QB7wCCZAA62RjYJsWvIjJEubSfZGL+T0yjWW06XyxV3bqxbYo\n" \
"Ob8VZRzI9neWagqNdwvYkQsEjgfbKbYK7p2CNTUQ\n" \
"-----END CERTIFICATE-----\n";

WiFiClient wifi;
HTTPClient http;
int status = WL_IDLE_STATUS;
String response;
int statusCode = 0;

void connectWifi(){
  WiFi.begin (ssid, password);
  Serial.print("Attempting to connect to Network named: ");
  Serial.println(ssid);
  display.drawString(5,5,"Connecting to WiFi");
  display.display();
  WiFi.mode(WIFI_STA);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
}

//Watchdog setup
const int loopTimeCtl = 21;
hw_timer_t *timer = NULL;
void IRAM_ATTR resetModule(){
    ets_printf("reboot\n");
    esp_restart_noos();
}
  
void setup() {
//  setup watchdog pin
  pinMode(loopTimeCtl, INPUT_PULLUP);
  pinMode(16,OUTPUT);
  digitalWrite(16, LOW); // set GPIO16 low to reset OLED
  delay(50);
  digitalWrite(16, HIGH);

  start_time = millis();
  delay(1000);
  timestamp = millis();

  display.init();
  display.flipScreenVertically();
  display.setFont(ArialMT_Plain_10);
  display.setTextAlignment(TEXT_ALIGN_LEFT);
  
  Serial.begin(115200);
//  while (!Serial); //if just the the basic function, must connect to a computer
  delay(1000);

//  attach watchdog setup
  timer = timerBegin(0, 80, true); //timer 0, div 80
  timerAttachInterrupt(timer, &resetModule, true);
  timerAlarmWrite(timer, 3000000, false); //set time in us
  timerAlarmEnable(timer); //enable interrupt
  
  connectWifi();
//  Serial.print("SSID: ");
//  Serial.println(WiFi.SSID());
  // print your WiFi shield's IP address:
  IPAddress ip = WiFi.localIP();
//  Serial.print("IP Address: ");
//  Serial.println(ip);
  display.drawString(5,5,"Connected to " + WiFi.SSID());
  display.display();
  display.drawString(5,25,"IP address " + String(ip));
  display.display();
  Token = getAuth();
  
//  Serial.println("LoRa Receiver");
  
  display.clear();
  display.setFont(ArialMT_Plain_10);
  display.drawString(5,5,"LoRa Receiver");
  display.display();
  SPI.begin(5,19,27,18);
  LoRa.setPins(SS,RST,DI0);

  if (!LoRa.begin(BAND)) {
    display.drawString(5,25,"Starting LoRa failed. Kill a kitten");
    while (1);
  }
//  Serial.println("LoRa Initialised. Pat a kitten");
//  
//  Serial.print("LoRa Frequency: ");
//  Serial.println(BAND);
//  
//  Serial.print("LoRa Spreading Factor: ");
//  Serial.println(spreadingFactor);
  LoRa.setSpreadingFactor(spreadingFactor);
  
//  Serial.print("LoRa Signal Bandwidth: ");
//  Serial.println(SignalBandwidth);
  LoRa.setSignalBandwidth(SignalBandwidth);

  LoRa.setCodingRate4(codingRateDenominator);
  
  display.drawString(5,25,"LoRa Initializing OK! Pat a kitten");
  display.display();
  new_rec = millis();
  old_rec = millis();
}

String getAuth() {
  String payload;
//  DynamicJsonBuffer  jsonBuffer(200);
  StaticJsonBuffer<200> jsonBuffer;
  JsonObject& creds = jsonBuffer.createObject();
  creds["username"] = API_user;
  creds["password"] = API_pass;
  creds.printTo(Serial);
  http.begin(SERVER_443_auth, root_ca);
  http.addHeader("Content-Type", "application/json");
  String input;
  creds.printTo(input);
  int httpCode = http.POST(input);
  // httpCode will be negative on error
  if(httpCode > 0) {
    // HTTP header has been send and Server response header has been handled
//    Serial.print("HTTP code = ");
//    Serial.println(httpCode);
    // file found at server
    if(httpCode == HTTP_CODE_OK) {
        payload = http.getString();
//        Serial.println(payload);
    }
  }else{
//    Serial.printf("[HTTP] POST... failed, error: %s\n", http.errorToString(httpCode).c_str());
  }
  http.end();;
//  parse jwt here
//https://github.com/bblanchon/ArduinoJson
  int len = payload.length();
  char json[len];
  payload.toCharArray(json, len);
  JsonObject& root = jsonBuffer.parseObject(json);
  if (!root.success()) {
//    Serial.println("parseObject() failed");
  }
  const char* jwt_token = root["access_token"];
//  Serial.println(jwt_token);
  return "Bearer "+ String(jwt_token);
}

String makeInput(String payload) {
  //build json object
  StaticJsonBuffer<500> jsonBuffer;
//  Serial.print("payload for sending to api is ");
//  Serial.println(payload);
  JsonObject& root = jsonBuffer.createObject();
  root["site"] = SITE;
  root["value"] = payload;
  root.printTo(Serial);
//  Serial.println();
  String input;
  root.printTo(input);
  return input;
}

void updateAPI(String payload) {
  if (payload.length() < 400) {
//    Serial.println("making POST request");
    http.begin(SERVER_443_data, root_ca);
    http.addHeader("Authorization", Token);
    http.addHeader("Content-Type", "application/json");
    String input = makeInput(payload);
    int httpCode = http.POST(input);
    // httpCode will be negative on error
    if(httpCode > 0) {
      // HTTP header has been send and Server response header has been handled
//      Serial.print("HTTP code = ");
//      Serial.println(httpCode);
      if(httpCode == 401){
        http.end();
        //token expired so get a new one
        Token = getAuth();
        //then do it all again
        http.begin(SERVER_443_data, root_ca);
        http.addHeader("Authorization", Token);
        int httpCode = http.POST(input);
      }
      // successful post
      if(httpCode == HTTP_CODE_OK) {
          String ret = http.getString();
//          Serial.println(ret);
      }else{
        //terminal so do nothing
        String ret = http.getString();
//        Serial.println(ret);
//        Serial.println("Failed to post on "+String(ret));
      }
    }else{
//      Serial.printf("[HTTP] POST... failed, error: %s\n", http.errorToString(httpCode).c_str());
    }
    http.end();
  }else{
//    Serial.println("payload too long, must be garbage");
  }
}

void loop() {
  timerWrite(timer, 0); //reset timer (feed watchdog)
  // set counters
  if ((millis() - timestamp) > COUNT_THRESH) {
    display.clear();
    display.setFont(ArialMT_Plain_10);
    unsigned long uptime = (millis() - start_time)/1000;
    hours = uptime/60/60;
    if (hours != 0) {
      mins = ((hours * 60 * 60) % uptime)/60;
    }else{
      mins = uptime / 60;
    }
    if (mins != 0) {
      secs = uptime % (mins * 60);
    }else{
      secs = uptime;
    } 
    time_disp = "Uptime is " + String(hours) + "h, " + String(mins) + "m, " + String(secs) +"s";
    display.drawString(3, 0, time_disp);
    display.drawString(20,22, data);
    display.drawString(0, 45, "Gap "+(String)minutes + "m, "+(String)seconds +"s, Pkt# " + (String)count);
    display.display();
    timestamp = millis();
  }
  // try to parse packet
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    old_rec = new_rec;
    new_rec = millis();
    count ++;
    // received a packet
//    Serial.print("Received packet. ");
    // read packet
    while (LoRa.available()) {
      data = LoRa.readString();
//      Serial.print(data);
      updateAPI(data);
    }
    
    // print RSSI of packet
//    Serial.print(" with RSSI ");
//    Serial.println(LoRa.packetRssi());
//    Serial.print(" with SNR ");
//    Serial.println(LoRa.packetSnr());

    unsigned long gap = (new_rec - old_rec)/1000;
    minutes = gap/60;
    seconds = gap % 60;       
  }
}
