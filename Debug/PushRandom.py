import argparse
import random
import socket
import string
import sys
import time

#!/usr/bin/env python3
"""
PushRandom.py
Send random binary data to 192.168.178.57:3615 and random text (length 16-17)
to 192.168.178.57:3617 for testing.
"""

DEFAULT_IP = "192.168.178.57"
PORT_BYTES = 3615
PORT_TEXT = 3614

def random_bytes(min_len=1, max_len=1024):
    length = random.randint(min_len, max_len)
    return random.randbytes(length) if hasattr(random, "randbytes") else bytes(random.getrandbits(8) for _ in range(length))

def random_text(length):
    return "".join(random.choices(string.ascii_letters + string.digits, k=length)).encode("utf-8")

def send_once(sock, addr, data):
    sock.sendto(data, addr)

def main():
    p = argparse.ArgumentParser(description="Send random payloads for testing.")
    p.add_argument("--host", "-H", default=DEFAULT_IP, help="Target IP (default %(default)s)")
    p.add_argument("--count", "-c", type=int, default=0, help="Number of iterations to send (0 = infinite, default 0)")
    p.add_argument("--interval", "-i", type=float, default=2.0, help="Seconds between iterations (default 2.0)")
    p.add_argument("--min-bytes", type=int, default=15, help="Min size for random byte array (default 1)")
    p.add_argument("--max-bytes", type=int, default=17, help="Max size for random byte array (default 1024)")
    args = p.parse_args()

    if args.min_bytes < 1 or args.max_bytes < args.min_bytes:
        print("Invalid byte size range.", file=sys.stderr)
        sys.exit(2)

    addr_bytes = (args.host, PORT_BYTES)
    addr_text = (args.host, PORT_TEXT)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        i = 0
        infinite = (args.count == 0)
        while infinite or i < args.count:
            b = random_bytes(args.min_bytes, args.max_bytes)
            send_once(sock, addr_bytes, b)

            text_len = random.randint(16, 17)
            t = random_text(text_len)
            send_once(sock, addr_text, t)

            i += 1
            print(f"[{i}/{args.count if not infinite else '∞'}] sent {len(b)} bytes -> {addr_bytes}, text({text_len}) -> {addr_text}")

            time.sleep(args.interval)
    finally:
        sock.close()

if __name__ == "__main__":
    main()