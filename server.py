import asyncio
from aiohttp import web
import aiofiles 
import logging

logging.basicConfig(level = logging.DEBUG)
import os


async def get_process(path):
    
        command = ['zip','-r','-',path]
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)
        return process
    
        
       
async def handle_index_page(request):
    async with aiofiles.open('index.html', mode='r') as index_file:
        index_contents = await index_file.read()
    return web.Response(text=index_contents, content_type='text/html')


async def get_archive(request):
    
    hash=request.match_info.get('archive_hash', "Anonymous")
    path=f"photos/{hash}/"
    
    if not os.path.exists(path):
        raise web.HTTPNotFound(text='Архив не существует или был удален')
    
    response = web.StreamResponse()
    
    response.headers['Content-Disposition:']='attachment; filename=archive.zip'
    await response.prepare(request)
    process=await get_process(path)
    try:
        while not process.stdout.at_eof():
            stdout = await process.stdout.read(n=100)
            
            await response.write(stdout)
        logging.info( 'Sending archive chunk' )
        return response
    except asyncio.CancelledError:
        logging.info( 'Download was interrupted' )
        raise
    finally:
        if  process.returncode is None:
            process.kill()
            process.communicate()
       
        

        
   


if __name__ == '__main__':
    app = web.Application()
    app.add_routes([
        web.get('/', handle_index_page),
        web.get('/archive/{archive_hash}/', get_archive),
       
    ])
    web.run_app(app)
