import asyncio

async def start_decision_loop(app):
    asyncio.create_task(_loop(app))

async def _loop(app):
    print("[Decision] Loop started")
    while True:
        await asyncio.sleep(1)
