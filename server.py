import os
import json
from aiohttp import web, WSMsgType

# Connected websocket clients pool
connected_clients = set()

async def handle_index(request):
    return web.Response(text='''
    <html>
    <head>
        <style>
            body { margin:0; background:#05070a; display:flex; flex-direction:column; justify-content:center; align-items:center; height:100vh; color:#00ffcc; font-family:monospace; }
            #log { margin-top:15px; font-size:13px; color:#00ffcc; border:1px solid rgba(0,255,204,0.4); padding:12px; border-radius:8px; width:85%; height:160px; overflow-y:auto; background:rgba(0,0,0,0.7); box-shadow: 0 0 10px rgba(0,255,204,0.1); }
            .key { color: #ff0055; font-weight: bold; }
            .val { color: #ffcc00; }
        </style>
    </head>
    <body>
        <h3 style="margin:0;">[✔] REALTIME GAMEPAD SOCKET SERVER ACTIVE</h3>
        <div id="log">> Waiting for Controller Signals...</div>

        <script>
            // Establish internal socket listener to display stream
            const protocol = location.protocol === 'https:' ? 'wss:' : 'ws:';
            const ws = new WebSocket(`${protocol}//${location.host}/ws`);

            ws.onmessage = (event) => {
                const log = document.getElementById('log');
                try {
                    const data = JSON.parse(event.data);
                    if (data.type === 'BUTTON' || data.type === 'AXIS') {
                        log.innerHTML += `<br>> [INPUT]: <span class="key">${data.key}</span> -> <span class="val">${data.value}</span>`;
                        log.scrollTop = log.scrollHeight;
                    }
                } catch(e) {}
            };
        </script>
    </body>
    </html>
    ''', content_type='text/html')

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    connected_clients.add(ws)

    try:
        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                data = msg.data
                # Broadcast incoming input to all connected sockets (including iframe display)
                for client in connected_clients:
                    if not client.closed:
                        await client.send_str(data)
            elif msg.type == WSMsgType.ERROR:
                print(f'WebSocket closed with exception {ws.exception()}')
    finally:
        connected_clients.remove(ws)

    return ws

app = web.Application()
app.router.add_get('/', handle_index)
app.router.add_get('/ws', websocket_handler)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    web.run_app(app, port=port)
    
