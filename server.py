import asyncio
from aiohttp import web
import datetime
import aiofiles 
INTERVAL_SECS = 1



async def cmd_run(command):
    proc = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    while not proc.stdout.at_eof():
        stdout = await proc.stdout.read(n=100)
        print(stdout)
        yield stdout


async def archive():
    command = 'zip - t.txt '
    async with aiofiles.open("archive.zip", "wb") as file:
        async for content in cmd_run(command):
            await file.write(content)






async def uptime_handler(request):
    
    response = web.StreamResponse()

    # Большинство браузеров не отрисовывают частично загруженный контент, только если это не HTML.
    # Поэтому отправляем клиенту именно HTML, указываем это в Content-Type.
    #response.headers['Content-Type'] = 'text/html'
    response.headers['Content-Disposition:']='attachment'
    # Отправляет клиенту HTTP заголовки
    await response.prepare(request)

    while True:
        formatted_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f'{formatted_date}<br>'  # <br> — HTML тег переноса строки

        # Отправляет клиенту очередную порцию ответа
        await response.write(message.encode('utf-8'))

        # await asyncio.sleep(INTERVAL_SECS)


if __name__ == '__main__':
    app = web.Application()
    app.add_routes([
        web.get('/', uptime_handler),
    ])
    web.run_app(app)
