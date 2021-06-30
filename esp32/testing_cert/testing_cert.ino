/*
 * Ensure TTGO LORA32-OLED V1 board selected
 * Process goes:
 * - capture data
 * - forward to api
 * - disply onsite data on OLED for Rob
 * - display time since last message
 */

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
//for base64 encoding creds
#include "base64.h"


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

//variables
const char sensorID[] = SENSOR_NAME;

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
String Token;
int statusCode = 0;

void connectWifi(){
  WiFi.begin (ssid, password);
  Serial.print("Attempting to connect to Network named: ");
  Serial.println(ssid);
  WiFi.mode(WIFI_STA);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
}
  
void setup() {
  Serial.begin(115200);
//  while (!Serial); //if just the the basic function, must connect to a computer
  delay(1000);
  
  connectWifi();
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());
  // print your WiFi shield's IP address:
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);
//  Token = getAuth();
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
  String auth = base64::encode(API_user + ":" + API_pass);
  http.addHeader("Authorization", "Basic " + auth);
  String input;
  creds.printTo(input);
//  Serial.println(input);
  int httpCode = http.POST(input);
  // httpCode will be negative on error
  if(httpCode > 0) {
    // HTTP header has been send and Server response header has been handled
    Serial.print("HTTP code = ");
    Serial.println(httpCode);
    // file found at server
    if(httpCode == HTTP_CODE_OK) {
        payload = http.getString();
        Serial.println(payload);
    }
  }else{
    Serial.printf("[HTTP] POST... failed, error: %s\n", http.errorToString(httpCode).c_str());
  }
  http.end();;
//  parse jwt here
//https://github.com/bblanchon/ArduinoJson
  int len = payload.length();
  char json[len];
  payload.toCharArray(json, len);
  JsonObject& root = jsonBuffer.parseObject(json);
  if (!root.success()) {
    Serial.println("parseObject() failed");
  }
  const char* jwt_token = root["access_token"];
  Serial.println(jwt_token);
//  return String(jwt_token);
  return "Bearer "+ String(jwt_token);
}

void updateAPI(String payload) {
  //Ensure token fits in here
//  DynamicJsonBuffer  jsonBuffer(500);
  StaticJsonBuffer<500> jsonBuffer;
  //build json object
  if (payload.length() < 100) {
    Serial.print("payload for sending to api is ");
    Serial.println(payload);
    JsonObject& root = jsonBuffer.createObject();
    root["site"] = SITE;
    root["value"] = payload;
    root.printTo(Serial);
    Serial.println();
    Serial.println("making POST request");
    http.begin(SERVER, root_ca);
    http.addHeader("Authorization", Token);
    http.addHeader("Content-Type", "application/json");
    String input;
    root.printTo(input);
    int httpCode = http.POST(input);
    // httpCode will be negative on error
    if(httpCode > 0) {
      // HTTP header has been send and Server response header has been handled
      Serial.print("HTTP code = ");
      Serial.println(httpCode);
      if(httpCode == 401){
        http.end();
        //token expired so get a new one
        Token = getAuth();
        //then do it all again
        http.begin(SERVER, root_ca);
        http.addHeader("Authorization", Token);
        http.addHeader("Content-Type", "application/json");
        String input;
        root.printTo(input);
        int httpCode = http.POST(input);
      }
      // successful post
      if(httpCode == HTTP_CODE_OK) {
          String payload = http.getString();
          Serial.println(payload);
      }else{
        //terminal so do nothing
        String payload = http.getString();
        Serial.println(payload);
        Serial.println("Failed to post on reauth "+String(payload));
      }
    }else{
      Serial.printf("[HTTP] POST... failed, error: %s\n", http.errorToString(httpCode).c_str());
    }
    http.end();
  }else{
    Serial.println("payload too long, must be garbage");
  }
}

void loop() {
  updateAPI("PY;6;R;3.94;");
  delay(10000);
}
