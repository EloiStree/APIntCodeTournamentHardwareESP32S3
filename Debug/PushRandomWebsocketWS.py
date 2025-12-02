# pc_client.py - Send random text and binary data to Pico W WebSocket
import asyncio
import websockets
import random
import struct
import time
import traceback

PICO_IP = "192.168.178.67"   # Change to your Pico's IP

async def random_sender():
    uri = f"ws://{PICO_IP}:80/ws"
    attempt = 0
    while True:
        attempt += 1
        print(f"[DEBUG] Attempting to connect to {uri} (attempt {attempt}) at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        try:
            async with websockets.connect(uri) as ws:
                print("[DEBUG] Connected to Pico W, entering send loop")
                loop_count = 0

                while True:
                    loop_count += 1
                    ts = asyncio.get_event_loop().time()

                    # Send random text
                    text = f"Random text {random.randint(1000, 9999)} @ {ts:.1f}"
                    print(f"[DEBUG] Sending text (len={len(text)}) -> {text!r}")
                    await ws.send(text)
                    print("[DEBUG] Sent text")

                    # Send random bytes (10 bytes)
                    binary = bytes(random.randint(0, 255) for _ in range(10))
                    print(f"[DEBUG] Sending binary (len={len(binary)}) -> {binary.hex()}")
                    await ws.send(binary)
                    print("[DEBUG] Sent bytes")

                    # Receive responses
                    try:
                        msg = await asyncio.wait_for(ws.recv(), timeout=1.0)
                        if isinstance(msg, bytes):
                            print(f"[DEBUG] Received bytes (len={len(msg)}) -> {msg.hex()}")
                        else:
                            print(f"[DEBUG] Received text (len={len(msg)}) -> {msg!r}")
                    except asyncio.TimeoutError:
                        print("[DEBUG] No message received within timeout")
                    except Exception as e:
                        print(f"[DEBUG] Error while receiving: {e}")
                        traceback.print_exc()

                    if loop_count % 10 == 0:
                        print(f"[DEBUG] Completed {loop_count} send cycles")

                    sleep_time = random.uniform(0.8, 2.5)
                    print(f"[DEBUG] Sleeping for {sleep_time:.2f}s before next send")
                    await asyncio.sleep(sleep_time)

        except (OSError, websockets.exceptions.InvalidURI,
                websockets.exceptions.InvalidHandshake,
                websockets.exceptions.ConnectionClosed) as e:
            print(f"[DEBUG] Connection error: {e}")
            traceback.print_exc()
        except Exception as e:
            print(f"[DEBUG] Unexpected error: {e}")
            traceback.print_exc()

        retry_delay = 5
        print(f"[DEBUG] Retrying in {retry_delay} seconds...")
        await asyncio.sleep(retry_delay)

if __name__ == "__main__":
    asyncio.run(random_sender())