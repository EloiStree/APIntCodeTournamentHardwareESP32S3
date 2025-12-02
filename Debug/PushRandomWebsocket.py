#!/usr/bin/env python3
"""
PushRandomWebSocket.py
Send random binary data and text via WebSocket to a server for testing.
"""

import argparse
import asyncio
import random
import string
import sys
import websockets

DEFAULT_HOST = "192.168.178.67"
DEFAULT_PORT = 5000
DEFAULT_PATH = "/input-iid"

def random_bytes(min_len=1, max_len=1024):
    """Generate random bytes."""
    length = random.randint(min_len, max_len)
    return random.randbytes(length) if hasattr(random, "randbytes") else bytes(random.getrandbits(8) for _ in range(length))

def random_text(length):
    """Generate random text string."""
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))

async def send_random_data(uri, args):
    """Connect to WebSocket and send random data."""
    try:
        async with websockets.connect(uri) as websocket:
            print(f"Connected to {uri}")
            
            i = 0
            infinite = (args.count == 0)
            
            while infinite or i < args.count:
                # Send random bytes as binary
                if args.send_binary:
                    b = random_bytes(args.min_bytes, args.max_bytes)
                    await websocket.send(b)
                    print(f"[{i+1}/{args.count if not infinite else '∞'}] Sent {len(b)} bytes (binary)")
                
                # Send random text
                if args.send_text:
                    text_len = random.randint(args.min_text, args.max_text)
                    t = random_text(text_len)
                    await websocket.send(t)
                    print(f"[{i+1}/{args.count if not infinite else '∞'}] Sent text (length {text_len}): {t}")
                
                # Try to receive response (non-blocking with timeout)
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=0.5)
                    print(f"  ← Received: {response}")
                except asyncio.TimeoutError:
                    pass  # No response, that's okay
                
                i += 1
                await asyncio.sleep(args.interval)
                
    except websockets.exceptions.WebSocketException as e:
        print(f"WebSocket error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    p = argparse.ArgumentParser(description="Send random payloads via WebSocket for testing.")
    p.add_argument("--host", "-H", default=DEFAULT_HOST, help="Target host (default %(default)s)")
    p.add_argument("--port", "-p", type=int, default=DEFAULT_PORT, help="WebSocket port (default %(default)s)")
    p.add_argument("--path", default=DEFAULT_PATH, help="WebSocket path (default %(default)s)")
    p.add_argument("--count", "-c", type=int, default=0, help="Number of iterations (0 = infinite, default 0)")
    p.add_argument("--interval", "-i", type=float, default=2.0, help="Seconds between sends (default 2.0)")
    
    # Binary data options
    p.add_argument("--send-binary", action="store_true", default=True, help="Send binary data (default True)")
    p.add_argument("--min-bytes", type=int, default=15, help="Min size for random bytes (default 15)")
    p.add_argument("--max-bytes", type=int, default=17, help="Max size for random bytes (default 17)")
    
    # Text data options
    p.add_argument("--send-text", action="store_true", default=True, help="Send text data (default True)")
    p.add_argument("--min-text", type=int, default=16, help="Min length for random text (default 16)")
    p.add_argument("--max-text", type=int, default=17, help="Max length for random text (default 17)")
    
    p.add_argument("--no-binary", dest="send_binary", action="store_false", help="Don't send binary data")
    p.add_argument("--no-text", dest="send_text", action="store_false", help="Don't send text data")
    
    args = p.parse_args()

    if args.min_bytes < 1 or args.max_bytes < args.min_bytes:
        print("Invalid byte size range.", file=sys.stderr)
        sys.exit(2)
    
    if args.min_text < 1 or args.max_text < args.min_text:
        print("Invalid text length range.", file=sys.stderr)
        sys.exit(2)

    if not args.send_binary and not args.send_text:
        print("Must enable at least one of --send-binary or --send-text", file=sys.stderr)
        sys.exit(2)

    # Build WebSocket URI
    uri = f"ws://{args.host}:{args.port}{args.path}"
    print(f"Connecting to {uri}...")

    # Run the async sender
    try:
        asyncio.run(send_random_data(uri, args))
    except KeyboardInterrupt:
        print("\nStopped by user")
        sys.exit(0)

if __name__ == "__main__":
    main()