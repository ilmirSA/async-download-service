import os
import subprocess

import asyncio
import aiofiles


async def cmd_run(command):
    proc = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    while not proc.stdout.at_eof():
        stdout = await proc.stdout.read(n=100)
        print(stdout)
        yield stdout


async def main():
    command = 'zip - t.txt '
    async with aiofiles.open("archive.zip", "wb") as file:
        async for content in cmd_run(command):
            await file.write(content)


if __name__ == '__main__':
    asyncio.run(main())
