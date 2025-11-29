
I learn from GPT that apparently my ESP32S3 can simulate XInput.

``` ino
#include <WiFi.h>
#include <WebServer.h>
#include <WiFiUdp.h>
#include <XInput.h>

const char* ssid     = "YOUR_SSID";
const char* password = "YOUR_PASS";

// Web server
WebServer server(80);

// UDP listener
WiFiUDP udp;
const unsigned int UDP_PORT = 4210;
char udpBuffer[256];


void applyCommand(const String &key, const String &value) {
    if (key == "lx") XInput.setJoystickX(0, value.toInt());
    else if (key == "ly") XInput.setJoystickY(0, value.toInt());
    else if (key == "rx") XInput.setJoystickX(1, value.toInt());
    else if (key == "ry") XInput.setJoystickY(1, value.toInt());

    else if (key == "a") {
        if (value == "1") XInput.press(BUTTON_A);
        else XInput.release(BUTTON_A);
    }

    else if (key == "b") {
        if (value == "1") XInput.press(BUTTON_B);
        else XInput.release(BUTTON_B);
    }

    else if (key == "lt") XInput.setTrigger(TRIGGER_LEFT, value.toInt());
    else if (key == "rt") XInput.setTrigger(TRIGGER_RIGHT, value.toInt());
}


void parseCommandString(String s) {
    // Expected format: "LX=1000;LY=-2000;A=1;RT=255;"
    while (s.length() > 0) {
        int eq = s.indexOf('=');
        int sc = s.indexOf(';');

        if (eq < 0 || sc < 0) break;

        String key = s.substring(0, eq);
        String val = s.substring(eq + 1, sc);

        key.toLowerCase();
        applyCommand(key, val);

        s = s.substring(sc + 1);
    }
}


void handleHTTPSet() {
    for (auto &arg : server.args()) {
        String key = server.argName(arg).toLowerCase();
        String value = server.arg(arg);
        applyCommand(key, value);
    }
    server.send(200, "text/plain", "OK");
}


void handleRoot() {
    server.send(200, "text/plain", "XInput QA Controller (HTTP + UDP)");
}


void setup() {
    Serial.begin(115200);

    // WiFi
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) delay(100);

    // HTTP
    server.on("/", handleRoot);
    server.on("/set", handleHTTPSet);
    server.begin();

    // UDP
    udp.begin(UDP_PORT);

    // XInput
    XInput.begin();
}


void loop() {
    // Handle HTTP
    server.handleClient();

    // Handle UDP
    int packetSize = udp.parsePacket();
    if (packetSize) {
        int len = udp.read(udpBuffer, sizeof(udpBuffer) - 1);
        if (len > 0) {
            udpBuffer[len] = '\0';
            parseCommandString(String(udpBuffer));
        }
    }

    delay(2);  // very fast poll
}


```
