# APIntCodeTournamentHardwareESP32S3
Simulate BLE Input and XInput 

Apparently you can simulate XInput with ESP32S3.
I have a version Arduino Leonardo but that dont have HTTP:

ESP32-BLE-Gamepad (lemmingDev fork)  
https://github.com/lemmingDev/ESP32-BLE-Gamepad  
NimBLE-Arduino 
https://github.com/h2zero/NimBLE-Arduino  
  
Some old code when I was doing some search on it:   
https://github.com/EloiStree/2024_11_31_ReadHardwareToIndexInteger/tree/main/   

I had an idea…
The ESP32 has the Bluetooth and Wi-Fi I need, and the Arduino Leonardo with XInput support is lacking those features.
Could I combine them so the ESP32 handles the keyboard and mouse, while the Arduino provides XInput?
