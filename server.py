import asyncio
from aiohttp import web
import aiofiles 
import logging

logging.basicConfig(level = logging.DEBUG)
import os


async def cmd_run(hash):
    command = f'zip -r - photos/{hash}/'
    proc = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    while not proc.stdout.at_eof():
        stdout = await proc.stdout.read(n=100)
        yield stdout

       
async def handle_index_page(request):
    async with aiofiles.open('index.html', mode='r') as index_file:
        index_contents = await index_file.read()
    return web.Response(text=index_contents, content_type='text/html')


async def get_archive(request):
   
    hash=request.match_info.get('archive_hash', "Anonymous")
    
    if not os.path.exists(f"photos/{hash}/"):
        raise web.HTTPNotFound(text='Архив не существует или был удален')
    
    response = web.StreamResponse()
    response.headers['Content-Disposition:']='attachment; filename=archive.zip'
    await response.prepare(request)
    async for data in cmd_run(hash):
        logging.info( 'Sending archive chunk' )
        await response.write(data)
        await asyncio.sleep(100)
    return response


if __name__ == '__main__':
    app = web.Application()
    app.add_routes([
        web.get('/', handle_index_page),
        web.get('/archive/{archive_hash}/', get_archive),
       
    ])
    web.run_app(app)
