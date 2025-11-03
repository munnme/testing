"""
OrangeCarrier WebSocket Test (Local Debug Version)
"""
import websocket
import json
import time

# 👉 এখানে সরাসরি তোমার টোকেন দাও (env ছাড়াই)
ORANGE_TOKEN = "eyJpdiI6IkduYWNQZm9iM0NKTEVNZXJYRjlORWc9PSIsInZhbHVlIjoiZkdNQXppVTA1Yk5lcG40NnZHRGhcL0NoRFJtenYwNHJjYXhzUUhzcHZ3KzFoZVN2MnpuOHowWThZd2w3azhWQXNPUFdORHMrdEVRNVh0T2FqcHNQMU9uU1J1dmZyR244RXhTSEFpT0JhQTQxSStxUGxYaGxidGE4M3Z4TXpUQlNBRzJYcXVYMjBESUpXWHY1OHFWdmg3T09MczZkRW5BXC81RnY5MlpidXNkRUxGXC9LQllqeXAzZndDQTBhWklnaVZyXC8zXC9yaTEzaDJcLytaUnUydzgyMCthSDlUNmtjbmVRbVRNdzcxbFRkbzJSZ3F5Y2pzeXM5NFg0QVhZM0Zka3NpZnJvSGZqazJFMnArZzVORmJBOFRcL3N3PT0iLCJtYWMiOiI3NTk5NDM4MDY2MGIyNTFkMzFlNDdjNzYwYmE3ZWU4Y2E4MmFiZGNkZWVkMGRhZDMyY2IzZWFmM2QzYjkwOGExIn0"

# 👉 টোকেন ইনকোড করে URL বানাও
WS_URL = f"wss://hub.orangecarrier.com/socket.io/?EIO=4&transport=websocket&token={ORANGE_TOKEN}"

print(f"\n🌐 Connecting to: {WS_URL}\n")

def on_open(ws):
    print("✅ Connected to OrangeCarrier WebSocket server!")

def on_message(ws, message):
    print("📩 Raw Message Received:")
    print(message[:500])  # প্রথম 500 অক্ষর দেখাও
    print("-" * 40)
    try:
        data = json.loads(message[1:]) if message.startswith("0") else json.loads(message)
        print("🧠 Parsed JSON:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except Exception as e:
        print("⚠️ Parse error:", e)

def on_error(ws, error):
    print("❌ WebSocket error:", error)

def on_close(ws, code, msg):
    print(f"🔴 WebSocket closed (code={code}, msg={msg}). Reconnecting in 5s...")
    time.sleep(5)
    start_ws()

def start_ws():
    ws = websocket.WebSocketApp(
        WS_URL,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever(ping_interval=20, ping_timeout=10)

if __name__ == "__main__":
    print("🚀 Starting WebSocket test client...\n")
    start_ws()
