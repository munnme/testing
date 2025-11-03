import socketio, time

ORANGE_TOKEN = "eyJpdiI6Ik5QSW5qU1RhY1kwQmwzcGY4T2NlV3c9PSIsInZhbHVlIjoicHpTVFQ2aG51TnJQQytlWkxJbElESnViTjFuaDZ6RlZVc1JORlpkcFwvMk8ySnlOQThzVEVLbnNlUmxYRlJhXC85T1FsbXBzSlJPaTlCV0pSWFkxNmcwUnV0R2Y4MEoyd1duTmpPdUpPK2U2bTA5OGxYVUh0ZVhReXkrUlRSRjkrdzV6R05aOTRsVTdoY1NrMHpycUFUbGttUGZoQWh2UEV1K21WXC9pb3cyVXI5MExPNDgxdE02NVNPMnNFTUlOeUJDQXZNY0RcL0xmT1lHemlQRWxPaGdiZzAzRzJrblwvTHNwRWVqQUtUcVdKRGdCQzhSXC80N3lXZERkOFo1Ym5SYWlBQW1aN0JRaUpPbklVd1hWSm5mQ1pSZGc9PSIsIm1hYyI6ImQ2MGQwOGFkNjJmOTE0OWYwMmRkNDhjZmVmNThlZmQ1NWJiMmQ1NjkxYjgwMGQ2MjYyZjY2NDhkNDNlMzljMTgifQ"  # সরাসরি এখানে দাও, env না
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
