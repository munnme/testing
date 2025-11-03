import websocket, socketio, threading, json, time, urllib.parse, ssl

ORANGE_TOKEN = "eyJpdiI6IjE1VTI2UE9aMEZqbDllNGRFQzBZY3c9PSIsInZhbHVlIjoiUGZJZFhZR3kza0o2bktRMUdqb1hSYTJ5SHRjXC9LcUVheEM4T1orbUxuWURRRHVJNVlibWRNOFpoY0tZVzJYdEpvSlhjODkyZTlFK1lSamtNZEkrRWZQU2NSbEY0Nmdyc1cyZEZrNVRXeVpRK2tqOWRWTXVuWlVUS3lGanVoVVZlRStxclcrRG9qR0M3RzlkNDR5cXdvUk1VK3RxdDVZVFBIbTl4Z1c1SmIxOTNGYUFaSmxtZFErTElZSlgycVwvTzJORVJlWFk4NU55Z1I2aDQ5ZkhLNld3UW13RkdFTUhVV1lHWFoxbmFyY1JNVGJlNDZlMEQ1YmRVdGRtY2I5ZmdjZVc0eWNDcjJqaUlobjdmWDVSV0YwUT09IiwibWFjIjoiMGZkODcxMjIzNzA1MWUyZjAzODE3OGZjZjMyN2YwYTk5N2U5ZmUxMjQzNzUxM2QxNzhlNjZhNWMxNmU1MWM1YyJ9"
encoded_token = urllib.parse.quote(ORANGE_TOKEN, safe='')
RAW_WS_URL = f"wss://hub.orangecarrier.com/socket.io/?EIO=4&transport=websocket&token={encoded_token}"
SIO_URL = "https://hub.orangecarrier.com"

def run_raw_socket():
    print("🧪 Trying RAW WebSocket mode...")

    def on_open(ws):
        print("✅ [RAW] Connected!")
        ws.send("40")
        ws.send(f'42["auth", {json.dumps({"token": ORANGE_TOKEN})}]')
        print("🔐 [RAW] Auth event sent.")

    def on_message(ws, msg):
        print("📩 [RAW]", msg)
        if msg == "2":
            ws.send("3")

    def on_error(ws, error):
        print("💥 [RAW] Error:", error)
        if "rsv" in str(error) or "opcode=8" in str(error) or "Connection reset" in str(error):
            print("⚠️ [RAW] Switching to Socket.IO mode...")
            ws.close()
            run_socketio()
        else:
            time.sleep(5)
            run_raw_socket()

    def on_close(ws, code, msg):
        print(f"🔴 [RAW] Closed ({code}, {msg}) → retrying in 5s...")
        time.sleep(5)
        run_raw_socket()

    ws = websocket.WebSocketApp(
        RAW_WS_URL,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )

    ws.run_forever(
        sslopt={"cert_reqs": ssl.CERT_NONE},
        skip_utf8_validation=True,
        ping_interval=25,
        ping_timeout=20
    )

def run_socketio():
    print("⚙️ Switching to Socket.IO Client mode...")
    sio = socketio.Client(logger=False, engineio_logger=False, reconnection=True)

    @sio.event
    def connect():
        print("✅ [SIO] Connected successfully!")
        sio.emit("auth", {"token": ORANGE_TOKEN})
        print("🔐 [SIO] Auth event sent.")

    @sio.event
    def disconnect():
        print("🔴 [SIO] Disconnected → retrying in 5s...")
        time.sleep(5)
        run_socketio()

    @sio.on("auth_response")
    def auth_response(data):
        print("🧠 [SIO] Auth Response:", data)

    try:
        sio.connect(SIO_URL, transports=["websocket"])
        sio.wait()
    except Exception as e:
        print("💥 [SIO] Error:", e)
        time.sleep(5)
        run_socketio()

if __name__ == "__main__":
    print("🚀 Starting OrangeCarrier Auto-Detect WebSocket Tester...\n")
    threading.Thread(target=run_raw_socket).start()
