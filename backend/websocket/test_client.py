import asyncio
import websockets

async def main():

    async with websockets.connect(
        "ws://127.0.0.1:8000/ws",
        ping_interval=None
    ) as websocket:

        await websocket.send(
            "Summarize the story"
        )

        print("\nAnswer:\n")

        while True:

            chunk = await websocket.recv()

            if chunk == "[END]":
                break

            print(chunk, end="", flush=True)

asyncio.run(main())