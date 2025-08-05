import asyncio
import asyncssh

HOST = '192.168.50.254'
USERNAME = 'oem'
PASSWORD = 'BytelOem'

async def tail_logread():
    async with asyncssh.connect(HOST, username=USERNAME, password=PASSWORD) as conn:
        async with conn.create_process('logread -f', term_type='xterm') as process:
            async for line in process.stdout:
                print(f"[logread] {line.strip()}")

async def run_command(command):
    async with asyncssh.connect(HOST, username=USERNAME, password=PASSWORD) as conn:
        result = await conn.run(command, check=True)
        print(f"[{command}] Output:\n{result.stdout.strip()}")

async def main():
    log_task = asyncio.create_task(tail_logread())
    await asyncio.sleep(2)  # Let logread start
    await run_command("wb_cli -s info")
    await asyncio.sleep(10)  # Let logs print for a while
    log_task.cancel()

asyncio.run(main())
