import asyncio, asyncssh

async def run():
    async with asyncssh.connect('192.168.50.254', username='oem', password="BytelOem") as conn:
        result = await conn.run('logread -f', check=True)
        print(result.stdout)

asyncio.run(run())