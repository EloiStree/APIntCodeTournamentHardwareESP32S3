import socket
import time

# Target IP: replace with your CircuitPython board's IP  http://192.168.178.67:5000
TARGET_IP = "192.168.178.70"   
TARGET_PORT = 3615

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print(f"Sending UDP packets to {TARGET_IP}:{TARGET_PORT}...")

def send_package_iid(int_value:int):
    #send litte-endian 4 byte integer
    byte_array = int_value.to_bytes(4, byteorder='little')
    sock.sendto(byte_array, (TARGET_IP, TARGET_PORT))


commands = [
    ["Random input for all gamepads, no menu", 1399, 2399],
    ["Enable hardware joystick ON/OFF", 1390, 2390],
    ["Press A button", 1300, 2300],
    ["Press X button", 1301, 2301],
    ["Press B button", 1302, 2302],
    ["Press Y button", 1303, 2303],
    ["Press left side button", 1304, 2304],
    ["Press right side button", 1305, 2305],
    ["Press left stick", 1306, 2306],
    ["Press right stick", 1307, 2307],
    ["Press menu right", 1308, 2308],
    ["Press menu left", 1309, 2309],
    ["Release D-pad", 1310, 2310],
    ["Press arrow north", 1311, 2311],
    ["Press arrow northeast", 1312, 2312],
    ["Press arrow east", 1313, 2313],
    ["Press arrow southeast", 1314, 2314],
    ["Press arrow south", 1315, 2315],
    ["Press arrow southwest", 1316, 2316],
    ["Press arrow west", 1317, 2317],
    ["Press arrow northwest", 1318, 2318],
    ["Press Xbox home button", 1319, 2319],
    ["Random axis", 1320, 2320],
    ["Start recording", 1321, 2321],
    ["Set left stick to neutral (clockwise)", 1330, 2330],
    ["Move left stick up", 1331, 2331],
    ["Move left stick up-right", 1332, 2332],
    ["Move left stick right", 1333, 2333],
    ["Move left stick down-right", 1334, 2334],
    ["Move left stick down", 1335, 2335],
    ["Move left stick down-left", 1336, 2336],
    ["Move left stick left", 1337, 2337],
    ["Move left stick up-left", 1338, 2338],
    ["Set right stick to neutral (clockwise)", 1340, 2340],
    ["Move right stick up", 1341, 2341],
    ["Move right stick up-right", 1342, 2342],
    ["Move right stick right", 1343, 2343],
    ["Move right stick down-right", 1344, 2344],
    ["Move right stick down", 1345, 2345],
    ["Move right stick down-left", 1346, 2346],
    ["Move right stick left", 1347, 2347],
    ["Move right stick up-left", 1348, 2348],
    ["Set left stick horizontal to 1.0", 1350, 2350],
    ["Set left stick horizontal to -1.0", 1351, 2351],
    ["Set left stick vertical to 1.0", 1352, 2352],
    ["Set left stick vertical to -1.0", 1353, 2353],
    ["Set right stick horizontal to 1.0", 1354, 2354],
    ["Set right stick horizontal to -1.0", 1355, 2355],
    ["Set right stick vertical to 1.0", 1356, 2356],
    ["Set right stick vertical to -1.0", 1357, 2357],
    ["Set left trigger to 100%", 1358, 2358],
    ["Set right trigger to 100%", 1359, 2359],
    ["Set left stick horizontal to 0.75", 1360, 2360],
    ["Set left stick horizontal to -0.75", 1361, 2361],
    ["Set left stick vertical to 0.75", 1362, 2362],
    ["Set left stick vertical to -0.75", 1363, 2363],
    ["Set right stick horizontal to 0.75", 1364, 2364],
    ["Set right stick horizontal to -0.75", 1365, 2365],
    ["Set right stick vertical to 0.75", 1366, 2366],
    ["Set right stick vertical to -0.75", 1367, 2367],
    ["Set left trigger to 75%", 1368, 2368],
    ["Set right trigger to 75%", 1369, 2369],
    ["Set left stick horizontal to 0.5", 1370, 2370],
    ["Set left stick horizontal to -0.5", 1371, 2371],
    ["Set left stick vertical to 0.5", 1372, 2372],
    ["Set left stick vertical to -0.5", 1373, 2373],
    ["Set right stick horizontal to 0.5", 1374, 2374],
    ["Set right stick horizontal to -0.5", 1375, 2375],
    ["Set right stick vertical to 0.5", 1376, 2376],
    ["Set right stick vertical to -0.5", 1377, 2377],
    ["Set left trigger to 50%", 1378, 2378],
    ["Set right trigger to 50%", 1379, 2379],
    ["Set left stick horizontal to 0.25", 1380, 2380],
    ["Set left stick horizontal to -0.25", 1381, 2381],
    ["Set left stick vertical to 0.25", 1382, 2382],
    ["Set left stick vertical to -0.25", 1383, 2383],
    ["Set right stick horizontal to 0.25", 1384, 2384],
    ["Set right stick horizontal to -0.25", 1385, 2385],
    ["Set right stick vertical to 0.25", 1386, 2386],
    ["Set right stick vertical to -0.25", 1387, 2387],
    ["Set left trigger to 25%", 1388, 2388],
    ["Set right trigger to 25%", 1389, 2389],
    ["Release ALL Touch", 1390, 2390],
    ["Release ALL Touch but menu", 1391, 2391],
    ["Clear Timed Command", 1398, 2398]
]


counter = 0
while True:
    message = f"Packet #{counter}".encode("utf-8")
    sock.sendto(message, (TARGET_IP, TARGET_PORT))
    print(f"Sent: {message}")
    counter += 1
    time.sleep(0.3)  # send one packet per second

    for command in commands:
        description, cmd_on, cmd_off = command
        print(f"Sending command: {description} (ON)")
        send_package_iid(cmd_on)
        time.sleep(0.3)  # wait half a second
        print(f"Sending command: {description} (OFF)")
        send_package_iid(cmd_off)
        time.sleep(0.3)  # wait half a second
