import socketio
import time
import urllib.parse

# =============================
# 🔐 CONFIGURATION
# =============================
ORANGE_TOKEN = "eyJpdiI6IkduYWNQZm9iM0NKTEVNZXJYRjlORWc9PSIsInZhbHVlIjoiZkdNQXppVTA1Yk5lcG40NnZHRGhcL0NoRFJtenYwNHJjYXhzUUhzcHZ3KzFoZVN2MnpuOHowWThZd2w3azhWQXNPUFdORHMrdEVRNVh0T2FqcHNQMU9uU1J1dmZyR244RXhTSEFpT0JhQTQxSStxUGxYaGxidGE4M3Z4TXpUQlNBRzJYcXVYMjBESUpXWHY1OHFWdmg3T09MczZkRW5BXC81RnY5MlpidXNkRUxGXC9LQllqeXAzZndDQTBhWklnaVZyXC8zXC9yaTEzaDJcLytaUnUydzgyMCthSDlUNmtjbmVRbVRNdzcxbFRkbzJSZ3F5Y2pzeXM5NFg0QVhZM0Zka3NpZnJvSGZqazJFMnArZzVORmJBOFRcL3N3PT0iLCJtYWMiOiI3NTk5NDM4MDY2MGIyNTFkMzFlNDdjNzYwYmE3ZWU4Y2E4MmFiZGNkZWVkMGRhZDMyY2IzZWFmM2QzYjkwOGExIn0"
encoded_token = urllib.parse.quote(ORANGE_TOKEN, safe='')
SERVER_URL = f"https://hub.orangecarrier.com?token={encoded_token}"

print(f"🚀 Starting OrangeCarrier Socket.IO test client...")
print(f"🌐 Connecting to: {SERVER_URL}\n")

# =============================
# ⚙️ Socket.IO Client
# =============================
sio = socketio.Client(reconnection=True, reconnection_attempts=0, reconnection_delay=5)

@sio.event
def connect():
    print("✅ [SIO] Connected successfully!")
    print("🔐 [SIO] Sending auth event...")
    sio.emit("auth", {"token": ORANGE_TOKEN})

@sio.on("auth_response")
def on_auth_response(data):
    print("🧠 [SIO] Auth response received:")
    print(data)

@sio.on("*")
def catch_all(event, data=None):
    print(f"📩 [SIO] Event received → {event}: {data}")

@sio.event
def disconnect():
    print("🔴 [SIO] Disconnected from server! Reconnecting...")

@sio.event
def connect_error(e):
    print(f"💥 [SIO] Connection error: {e}")

# =============================
# 🚀 Start Client
# =============================
while True:
    try:
        sio.connect(SERVER_URL, transports=["websocket"])
        sio.wait()
    except Exception as e:
        print(f"⚠️ [SIO] Connection lost: {e}")
        print("🔁 Retrying in 5s...\n")
        time.sleep(5)
