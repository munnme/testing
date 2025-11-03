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
# 🔁 STABLE SOCKET.IO WRAPPER
# =============================

def run_socket():
    def send_heartbeat(ws):
        """Periodically send ping to keep connection alive"""
        while ws.keep_running:
            time.sleep(25)
            try:
                print("📤 Sending heartbeat ping (type=2)")
                ws.send("2")  # socket.io ping
            except Exception as e:
                print("⚠️ Ping failed:", e)
                break

    def keep_alive_event(ws):
        """Send dummy event to stay authorized"""
        while ws.keep_running:
            time.sleep(15)
            try:
                msg = '42["ping","keepalive"]'
                ws.send(msg)
                print("📡 Sent keepalive event:", msg)
            except Exception as e:
                print("⚠️ Keepalive failed:", e)
                break

    def on_open(ws):
        print("✅ Connected to OrangeCarrier WebSocket!")
        ws.send("40")  # complete socket.io connect
        threading.Thread(target=send_heartbeat, daemon=True).start()
        threading.Thread(target=keep_alive_event, daemon=True).start()

    def on_message(ws, message):
        print("📩 Received:", message)
        try:
            if message.startswith("0"):
                info = json.loads(message[1:])
                print("🧠 Handshake info:", json.dumps(info, indent=2))
                ws.send("40")  # confirm ready
            elif message.startswith("42"):
                print("📡 Event:", message)
            elif message == "2":
                print("↔️ Ping from server → sending pong")
                ws.send("3")
        except Exception as e:
            print("⚠️ Message parse error:", e)

    def on_close(ws, code, msg):
        print(f"🔴 Disconnected (code={code}, msg={msg}) → reconnecting in 5s...\n")
        time.sleep(5)
        run_socket()

    def on_error(ws, error):
        print("💥 WebSocket error:", error)

    ws = websocket.WebSocketApp(
        WS_URL,
        on_open=on_open,
        on_message=on_message,
        on_close=on_close,
        on_error=on_error
    )

    ws.run_forever(
        ping_interval=25,
        ping_timeout=20,
        sslopt={"cert_reqs": 0}
    )


# =============================
# 🚀 START CLIENT
# =============================
if __name__ == "__main__":
    print("🚀 Starting stable OrangeCarrier WebSocket test client...\n")
    run_socket()
