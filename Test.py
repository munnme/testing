import websocket
import threading
import time
import json
import urllib.parse

# =============================
# 🔐 CONFIGURATION
# =============================
ORANGE_TOKEN = "eyJpdiI6IkduYWNQZm9iM0NKTEVNZXJYRjlORWc9PSIsInZhbHVlIjoiZkdNQXppVTA1Yk5lcG40NnZHRGhcL0NoRFJtenYwNHJjYXhzUUhzcHZ3KzFoZVN2MnpuOHowWThZd2w3azhWQXNPUFdORHMrdEVRNVh0T2FqcHNQMU9uU1J1dmZyR244RXhTSEFpT0JhQTQxSStxUGxYaGxidGE4M3Z4TXpUQlNBRzJYcXVYMjBESUpXWHY1OHFWdmg3T09MczZkRW5BXC81RnY5MlpidXNkRUxGXC9LQllqeXAzZndDQTBhWklnaVZyXC8zXC9yaTEzaDJcLytaUnUydzgyMCthSDlUNmtjbmVRbVRNdzcxbFRkbzJSZ3F5Y2pzeXM5NFg0QVhZM0Zka3NpZnJvSGZqazJFMnArZzVORmJBOFRcL3N3PT0iLCJtYWMiOiI3NTk5NDM4MDY2MGIyNTFkMzFlNDdjNzYwYmE3ZWU4Y2E4MmFiZGNkZWVkMGRhZDMyY2IzZWFmM2QzYjkwOGExIn0"
encoded_token = urllib.parse.quote(ORANGE_TOKEN, safe='')
WS_URL = f"wss://hub.orangecarrier.com/socket.io/?EIO=4&transport=websocket&token={encoded_token}"

print(f"🌐 Connecting to: {WS_URL}\n")

# =============================
# 🔁 AUTO RECONNECT WRAPPER
# =============================
def run_socket():
    def on_open(ws):
        print("✅ Connected to OrangeCarrier WebSocket!")

        # Socket.IO handshake confirm
        ws.send("40")

        # Authorization event পাঠাও
        auth_payload = json.dumps({"token": ORANGE_TOKEN})
        ws.send(f'42["auth", {auth_payload}]')
        print("🔐 Sent auth event to server.")

        # Custom heartbeat thread
        def send_heartbeat():
            while ws.keep_running:
                time.sleep(25)
                try:
                    print("📤 Sending custom ping (Socket.IO style)...")
                    ws.send('42["ping"]')
                except Exception as e:
                    print("⚠️ Heartbeat failed:", e)
                    break
        threading.Thread(target=send_heartbeat, daemon=True).start()

    def on_message(ws, message):
        print("📩 Received:", message)

        # Handshake (0{json})
        if message.startswith("0"):
            try:
                data = json.loads(message[1:])
                print("🧠 Handshake info:", json.dumps(data, indent=2))
            except Exception:
                pass

        # Ping from server
        elif message == "2":
            print("↔️ Ping from server → sending pong")
            ws.send("3")

        # Custom server response
        elif message.startswith("42"):
            print("📡 Socket.IO event:", message)

    def on_error(ws, error):
        print("💥 WebSocket error:", error)

    def on_close(ws, code, msg):
        print(f"🔴 Disconnected (code={code}, msg={msg}) → reconnecting in 5s...")
        time.sleep(5)
        run_socket()  # auto reconnect

    ws = websocket.WebSocketApp(
        WS_URL,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )

    ws.run_forever(
        ping_interval=25,
        ping_timeout=20,
        sslopt={"cert_reqs": 0}  # ignore SSL warnings
    )

# =============================
# 🚀 MAIN
# =============================
if __name__ == "__main__":
    print("🚀 Starting stable OrangeCarrier WebSocket test client...")
    run_socket()
