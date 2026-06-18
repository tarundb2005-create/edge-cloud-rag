import asyncio
import websockets

async def main():

    async with websockets.connect(
        "ws://127.0.0.1:8000/ws",
        ping_interval=None
    ) as websocket:

        await websocket.send("Summarize the story")

        answer = await websocket.recv()

        print("\nAnswer:\n")
        print(answer)

asyncio.run(main())