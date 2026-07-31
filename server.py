import os
from aiohttp import web

async def handle_index(request):
    return web.Response(text='''
    <html>
    <head>
        <style>
            body { margin:0; background:#05070a; display:flex; justify-content:center; align-items:center; height:100vh; overflow:hidden; }
            h1 { color: #00ffcc; font-family: sans-serif; text-shadow: 0 0 15px #00ffcc; font-size: 20px; letter-spacing: 2px; }
        </style>
    </head>
    <body>
        <h1>[✔] PERMANENT CLOUD SERVER ACTIVE</h1>
    </body>
    </html>
    ''', content_type='text/html')

app = web.Application()
app.router.add_get('/', handle_index)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    web.run_app(app, port=port)
