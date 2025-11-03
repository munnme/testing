import websocket
import threading
import time
import json
import urllib.parse
import os

# =============================
# 🔐 CONFIGURATION
# =============================
# এখানে তোমার নতুন OrangeCarrier token দাও ↓
ORANGE_TOKEN = "eyJpdiI6IkduYWNQZm9iM0NKTEVNZXJYRjlORWc9PSIsInZhbHVlIjoiZkdNQXppVTA1Yk5lcG40NnZHRGhcL0NoRFJtenYwNHJjYXhzUUhzcHZ3KzFoZVN2MnpuOHowWThZd2w3azhWQXNPUFdORHMrdEVRNVh0T2FqcHNQMU9uU1J1dmZyR244RXhTSEFpT0JhQTQxSStxUGxYaGxidGE4M3Z4TXpUQlNBRzJYcXVYMjBESUpXWHY1OHFWdmg3T09MczZkRW5BXC81RnY5MlpidXNkRUxGXC9LQllqeXAzZndDQTBhWklnaVZyXC8zXC9yaTEzaDJcLytaUnUydzgyMCthSDlUNmtjbmVRbVRNdzcxbFRkbzJSZ3F5Y2pzeXM5NFg0QVhZM0Zka3NpZnJvSGZqazJFMnArZzVORmJBOFRcL3N3PT0iLCJtYWMiOiI3NTk5NDM4MDY2MGIyNTFkMzFlNDdjNzYwYmE3ZWU4Y2E4MmFiZGNkZWVkMGRhZDMyY2IzZWFmM2QzYjkwOGExIn0"
encoded_token = urllib.parse.quote(ORANGE_TOKEN, safe='')

WS_URL = f"wss://hub.orangecarrier.com/socket.io/?EIO=4&transport=websocket&token={encoded_token}"
print(f"🌐 Connecting to: {WS_URL}\n")

# =============================
# 🔁 AUTO RECONNECT WRAPPER
# =============================

def run_socket():
    def on_open(ws):
        print("✅ Connected to OrangeCarrier WebSocket server!")
        ws.send("40")  # Socket.IO connect handshake

        # Start background pinger
        def ping_loop():
            while ws.keep_running:
                time.sleep(25)
                try:
                    print("📤 Sending ping...")
                    ws.send("2")
                except Exception as e:
                    print("⚠️ Ping failed:", e)
                    break
        threading.Thread(target=ping_loop, daemon=True).start()

    def on_message(ws, message):
        print("📩 Message:", message)
        if message.startswith("0"):
            try:
                data = json.loads(message[1:])
                print("🧠 Handshake info:", json.dumps(data, indent=2))
            except:
                pass
            ws.send("40")  # Confirm connect again
        elif message == "2":
            print("📩 Received ping from server -> sending pong")
            ws.send("3")

    def on_close(ws, close_status_code, close_msg):
        print(f"🔴 Disconnected! Code={close_status_code}, Msg={close_msg}")
        print("🔁 Reconnecting in 5s...\n")
        time.sleep(5)
        run_socket()

    def on_error(ws, error):
        print("💥 WebSocket error:", error)

    # Create websocket client
    ws = websocket.WebSocketApp(
        WS_URL,
        on_open=on_open,
        on_message=on_message,
        on_close=on_close,
        on_error=on_error,
    )

    ws.run_forever(
        ping_interval=25,
        ping_timeout=20,
        sslopt={"cert_reqs": 0}  # Disable SSL verify for test
    )

# =============================
# 🚀 START SOCKET CLIENT
# =============================
if __name__ == "__main__":
    print("🚀 Starting OrangeCarrier WebSocket test client...")
    run_socket()
