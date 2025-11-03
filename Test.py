import socketio
import time
import urllib.parse

# =============================
# 🔐 CONFIGURATION
# =============================
ORANGE_TOKEN = "eyJpdiI6IjE1VTI2UE9aMEZqbDllNGRFQzBZY3c9PSIsInZhbHVlIjoiUGZJZFhZR3kza0o2bktRMUdqb1hSYTJ5SHRjXC9LcUVheEM4T1orbUxuWURRRHVJNVlibWRNOFpoY0tZVzJYdEpvSlhjODkyZTlFK1lSamtNZEkrRWZQU2NSbEY0Nmdyc1cyZEZrNVRXeVpRK2tqOWRWTXVuWlVUS3lGanVoVVZlRStxclcrRG9qR0M3RzlkNDR5cXdvUk1VK3RxdDVZVFBIbTl4Z1c1SmIxOTNGYUFaSmxtZFErTElZSlgycVwvTzJORVJlWFk4NU55Z1I2aDQ5ZkhLNld3UW13RkdFTUhVV1lHWFoxbmFyY1JNVGJlNDZlMEQ1YmRVdGRtY2I5ZmdjZVc0eWNDcjJqaUlobjdmWDVSV0YwUT09IiwibWFjIjoiMGZkODcxMjIzNzA1MWUyZjAzODE3OGZjZjMyN2YwYTk5N2U5ZmUxMjQzNzUxM2QxNzhlNjZhNWMxNmU1MWM1YyJ9"
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
    # তুমি চাইলে নিচের লাইনগুলোও ট্রাই করতে পারো:
    # sio.emit("authenticate", {"token": ORANGE_TOKEN})
    # sio.emit("authorization", {"token": ORANGE_TOKEN})

@sio.event
def disconnect():
    print("🔴 [SIO] Disconnected from server! Reconnecting...")

@sio.event
def connect_error(e):
    print(f"💥 [SIO] Connection error: {e}")

# =============================
# 📡 Catch All Incoming Events
# =============================
@sio.on("*")
def catch_all(event, data=None):
    print(f"📩 [SIO] Event received → {event}: {data}")

@sio.on("auth_response")
def on_auth_response(data):
    print("🧠 [SIO] Auth response received:")
    print(data)

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
