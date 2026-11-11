# Realtime Gamepad Socket Server

A small Python prototype that receives controller input over WebSockets and broadcasts input events to connected browser clients.

## What it currently demonstrates

- An aiohttp web server
- A WebSocket endpoint for connected clients
- Broadcasting incoming text messages to connected sockets
- A minimal browser page that displays parsed button and axis events

## Requirements

- Python 3
- aiohttp

## Run locally

Install the dependency:

```bash
python -m pip install aiohttp
```

Start the server:

```bash
python server.py
```

Open the local server address shown by the application in a browser, then connect a compatible controller client to the WebSocket endpoint.

## Status and limitations

This is a realtime input-transport prototype, not a complete cloud-gaming platform. It does not itself provide game streaming, video encoding, authentication, session isolation, or production-grade WebSocket security.

Only connect trusted clients on a network you control. Add authentication, input validation, origin checks, rate limits, and secure transport before exposing it beyond a local test environment.