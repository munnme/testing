import socketio
import urllib.parse
import time

# ======================
# 🔐 CONFIGURATION
# ======================
ORANGE_TOKEN = "eyJpdiI6IkduYWNQZm9iM0NKTEVNZXJYRjlORWc9PSIsInZhbHVlIjoiZkdNQXppVTA1Yk5lcG40NnZHRGhcL0NoRFJtenYwNHJjYXhzUUhzcHZ3KzFoZVN2MnpuOHowWThZd2w3azhWQXNPUFdORHMrdEVRNVh0T2FqcHNQMU9uU1J1dmZyR244RXhTSEFpT0JhQTQxSStxUGxYaGxidGE4M3Z4TXpUQlNBRzJYcXVYMjBESUpXWHY1OHFWdmg3T09MczZkRW5BXC81RnY5MlpidXNkRUxGXC9LQllqeXAzZndDQTBhWklnaVZyXC8zXC9yaTEzaDJcLytaUnUydzgyMCthSDlUNmtjbmVRbVRNdzcxbFRkbzJSZ3F5Y2pzeXM5NFg0QVhZM0Zka3NpZnJvSGZqazJFMnArZzVORmJBOFRcL3N3PT0iLCJtYWMiOiI3NTk5NDM4MDY2MGIyNTFkMzFlNDdjNzYwYmE3ZWU4Y2E4MmFiZGNkZWVkMGRhZDMyY2IzZWFmM2QzYjkwOGExIn0"
encoded_token = urllib.parse.quote(ORANGE_TOKEN, safe="")
WS_URL = f"wss://hub.orangecarrier.com/socket.io/?EIO=4&transport=websocket&token={encoded_token}"

print(f"🌐 Connecting to: {WS_URL}")

# ======================
# ⚙️ Socket.IO Client
# ======================
sio = socketio.Client(logger=True, engineio_logger=True)

@sio.event
def connect():
    print("✅ [SIO] Connected successfully!")
    print("🔐 [SIO] Sending auth event...")
    try:
        sio.emit("auth", {"token": ORANGE_TOKEN})
    except Exception as e:
        print("⚠️ Auth emit failed:", e)

@sio.event
def connect_error(data):
    print("❌ Connection failed:", data)

@sio.event
def disconnect():
    print("🔴 Disconnected from server!")

# ======================
# 🧠 AUTH RESPONSE HANDLER
# ======================
@sio.on("auth_success")
def auth_success(data):
    print("✅✅ AUTH PASSED! You are inside the panel.")
    print("🔸 Server response:", data)

@sio.on("auth_error")
def auth_error(data):
    print("❌ AUTH FAILED! Invalid token or access denied.")
    print("🔹 Server response:", data)

# fallback for any unknown message
@sio.on("*")
def catch_all(event, data=None):
    print(f"📩 [EVENT] {event}: {data}")

# ======================
# 🚀 START CONNECTION
# ======================
try:
    print("🚀 Starting OrangeCarrier Auth Tester...")
    sio.connect(WS_URL, transports=["websocket"])
    sio.wait()
except Exception as e:
    print("💥 Fatal error:", e)
    time.sleep(10)
