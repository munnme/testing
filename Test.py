import socketio, time

ORANGE_TOKEN = "eyJpdiI6IkduYWNQZm9iM0NKTEVNZXJYRjlORWc9PSIsInZhbHVlIjoiZkdNQXppVTA1Yk5lcG40NnZHRGhcL0NoRFJtenYwNHJjYXhzUUhzcHZ3KzFoZVN2MnpuOHowWThZd2w3azhWQXNPUFdORHMrdEVRNVh0T2FqcHNQMU9uU1J1dmZyR244RXhTSEFpT0JhQTQxSStxUGxYaGxidGE4M3Z4TXpUQlNBRzJYcXVYMjBESUpXWHY1OHFWdmg3T09MczZkRW5BXC81RnY5MlpidXNkRUxGXC9LQllqeXAzZndDQTBhWklnaVZyXC8zXC9yaTEzaDJcLytaUnUydzgyMCthSDlUNmtjbmVRbVRNdzcxbFRkbzJSZ3F5Y2pzeXM5NFg0QVhZM0Zka3NpZnJvSGZqazJFMnArZzVORmJBOFRcL3N3PT0iLCJtYWMiOiI3NTk5NDM4MDY2MGIyNTFkMzFlNDdjNzYwYmE3ZWU4Y2E4MmFiZGNkZWVkMGRhZDMyY2IzZWFmM2QzYjkwOGExIn0"  # সরাসরি এখানে দাও, env না
WS_URL = f"wss://hub.orangecarrier.com/socket.io/?EIO=4&transport=websocket&token={ORANGE_TOKEN}"

print("🌐 Connecting to:", WS_URL)

sio = socketio.Client(logger=True, engineio_logger=True)

@sio.event
def connect():
    print("✅ Connected successfully!")

@sio.event
def disconnect():
    print("🔴 Disconnected!")

@sio.event
def connect_error(e):
    print("❌ Connection error:", e)

try:
    sio.connect(WS_URL, transports=["websocket"])
    sio.wait()
except Exception as e:
    print("💥 Error:", e)
    time.sleep(5)
