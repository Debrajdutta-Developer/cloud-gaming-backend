import os
import json
from aiohttp import web, WSMsgType

async def handle_index(request):
    return web.Response(text='''
    <html>
    <head>
        <style>
            body { margin:0; background:#05070a; display:flex; flex-direction:column; justify-content:center; align-items:center; height:100vh; color:#00ffcc; font-family:monospace; }
            #log { margin-top:20px; font-size:14px; color:#aaa; border:1px solid rgba(0,255,204,0.3); padding:15px; border-radius:8px; width:80%; height:150px; overflow-y:auto; background:rgba(0,0,0,0.5); }
        </style>
    </head>
    <body>
        <h2>[✔] REALTIME GAMEPAD SOCKET SERVER ACTIVE</h2>
        <div id="log">> Listening for Controller Input Stream...</div>
        <script>
            // Internal Stream Monitor Logic
            window.addEventListener('message', (e) => {
                const log = document.getElementById('log');
                log.innerHTML += '<br>' + JSON.stringify(e.data);
                log.scrollTop = log.scrollHeight;
            });
        </script>
    </body>
    </html>
    ''', content_type='text/html')

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    print("=== GAMEPAD CONNECTED VIA WEBSOCKET ===")

    async for msg in ws:
        if msg.type == WSMsgType.TEXT:
            data = json.loads(msg.data)
            # Log Incoming Controller Data in Backend Console
            print(f"[INPUT RECEIVED]: {data}")
            # Echo back confirmation to frontend
            await ws.send_str(json.dumps({"status": "ACK", "received": data}))
        elif msg.type == WSMsgType.ERROR:
            print(f'WebSocket connection closed with exception {ws.exception()}')

    return ws

app = web.Application()
app.router.add_get('/', handle_index)
app.router.add_get('/ws', websocket_handler)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    web.run_app(app, port=port)
    
