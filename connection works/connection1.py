import asyncio
import asyncssh

# Shared device credentials
HOST = '192.168.50.254'
USERNAME = 'oem'
PASSWORD = 'BytelOem'

async def tail_logread():
    """Persistent background task to read logs"""
    async with asyncssh.connect(HOST, username=USERNAME, password=PASSWORD) as conn:
        async with conn.create_process('logread -f') as process:
            async for line in process.stdout:
                print(f"[logread] {line.strip()}")

async def run_command(command):
    """Run a one-shot command like wb_cli"""
    async with asyncssh.connect(HOST, username=USERNAME, password=PASSWORD) as conn:
        result = await conn.run(command, check=True)
        print(f"[{command}] Output:\n{result.stdout.strip()}")

async def main():
    # Run logread in background
    log_task = asyncio.create_task(tail_logread())

    # Wait a bit (simulate staggered start)
    await asyncio.sleep(2)

    # Run other command concurrently
    await run_command("wb_cli -s info")

    # Wait as long as you want for logread
    await asyncio.sleep(20)  # Change to `await log_task` if you want it to run forever

    log_task.cancel()  # Cancel logread when done (optional)

asyncio.run(main())
