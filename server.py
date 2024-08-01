import asyncio
from aiohttp import web
import aiofiles 
import logging
import argparse

from functools import partial
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


async def get_archive(request,delay,path):
    
    hash=request.match_info.get('archive_hash', None)
    path=f"{path}/{hash}/"
    
    if not os.path.exists(path)or not hash:
        raise web.HTTPNotFound(text='Архив не существует или был удален')
    
    response = web.StreamResponse()
    
    response.headers['Content-Disposition:']='attachment; filename=archive.zip'
    await response.prepare(request)
    process=await get_process(path)

    if delay:
        await asyncio.sleep(delay)

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


    parser = argparse.ArgumentParser(
        description="Создает из ссылки битлинк или показывает кол-во переходов по битлинку")
    parser.add_argument('-l', '--logging', type=bool,default='True')
    parser.add_argument('-d', '--delay', type=int, default=None)
    parser.add_argument('-p', '--path', type=str,default='photos')
    args = parser.parse_args()

    if args.logging:
        logging.basicConfig(level=logging.INFO)

    app = web.Application()
    app.add_routes([
        web.get('/', handle_index_page),
        web.get('/archive/{archive_hash}/', partial(get_archive,delay=args.delay,path=args.path)),
       
    ])
    web.run_app(app)
