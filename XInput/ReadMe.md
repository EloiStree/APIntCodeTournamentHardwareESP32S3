
I learn from GPT that apparently my ESP32S3 can simulate XInput.

```
#include <WiFi.h>
#include <WebServer.h>
#include <XInput.h>

const char* ssid     = "YOUR_SSID";
const char* password = "YOUR_PASS";

WebServer server(80);

void handleRoot() {
    server.send(200, "text/plain", "XInput QA Controller Active");
}

void handleSet() {
    if (server.hasArg("lx")) {
        XInput.setJoystickX(0, server.arg("lx").toInt());
    }
    if (server.hasArg("ly")) {
        XInput.setJoystickY(0, server.arg("ly").toInt());
    }
    if (server.hasArg("rx")) {
        XInput.setJoystickX(1, server.arg("rx").toInt());
    }
    if (server.hasArg("ry")) {
        XInput.setJoystickY(1, server.arg("ry").toInt());
    }

    if (server.hasArg("a")) {
        if (server.arg("a") == "1") XInput.press(BUTTON_A);
        else XInput.release(BUTTON_A);
    }

    if (server.hasArg("lt"))
        XInput.setTrigger(TRIGGER_LEFT, server.arg("lt").toInt());
    if (server.hasArg("rt"))
        XInput.setTrigger(TRIGGER_RIGHT, server.arg("rt").toInt());

    server.send(200, "text/plain", "OK");
}

void setup() {
    Serial.begin(115200);
    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        delay(250);
    }

    server.on("/", handleRoot);
    server.on("/set", handleSet);
    server.begin();

    XInput.begin();
}

void loop() {
    server.handleClient();
    delay(5);
}

```
