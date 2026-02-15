import asyncio, asyncssh

async def run(command):
    async with asyncssh.connect('192.168.50.254', username='oem', password="BytelOem") as conn:
        result = await conn.run(command, check=True)
        print(result.stdout)

asyncio.run(run("wb_cli -s info"))