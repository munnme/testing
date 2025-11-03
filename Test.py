import socketio
import urllib.parse
import time

# ======================
# 🔐 CONFIGURATION
# ======================
ORANGE_TOKEN = "eyJpdiI6IjE1VTI2UE9aMEZqbDllNGRFQzBZY3c9PSIsInZhbHVlIjoiUGZJZFhZR3kza0o2bktRMUdqb1hSYTJ5SHRjXC9LcUVheEM4T1orbUxuWURRRHVJNVlibWRNOFpoY0tZVzJYdEpvSlhjODkyZTlFK1lSamtNZEkrRWZQU2NSbEY0Nmdyc1cyZEZrNVRXeVpRK2tqOWRWTXVuWlVUS3lGanVoVVZlRStxclcrRG9qR0M3RzlkNDR5cXdvUk1VK3RxdDVZVFBIbTl4Z1c1SmIxOTNGYUFaSmxtZFErTElZSlgycVwvTzJORVJlWFk4NU55Z1I2aDQ5ZkhLNld3UW13RkdFTUhVV1lHWFoxbmFyY1JNVGJlNDZlMEQ1YmRVdGRtY2I5ZmdjZVc0eWNDcjJqaUlobjdmWDVSV0YwUT09IiwibWFjIjoiMGZkODcxMjIzNzA1MWUyZjAzODE3OGZjZjMyN2YwYTk5N2U5ZmUxMjQzNzUxM2QxNzhlNjZhNWMxNmU1MWM1YyJ9"
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
