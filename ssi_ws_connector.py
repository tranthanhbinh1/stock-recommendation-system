import asyncio
import websockets

async def client():
    uri = "wss://txnstream-iboard.ssi.com.vn/realtime"
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello, Server!")
        response = await websocket.recv()
        print(f"Received: {response}")

asyncio.get_event_loop().run_until_complete(client())
