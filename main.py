import os
import subprocess



args=["zip","-",'t.txt' ]
procces=subprocess.Popen(args,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
a,b=procces.communicate()
print(a,b)

# print(data)
# code=procces.wait()
# args=[f'zip', 'archive.zip <<',]
# subprocess.call(args,stdin=archive)

# with open("t.zip","wb") as file:
#     file.write(archive)
# args=['zip','a.zip',file]


# with open("t.zip","wb") as file:
   
#     args=['zip','a.zip',file]
#     subprocess.call(args=args, shell=True)

# import asyncio


# async def cmd_run(command):
#     proc = await asyncio.create_subprocess_shell(
#         command,
#         stdout=asyncio.subprocess.PIPE,
#         stderr=asyncio.subprocess.PIPE)
    
#     stdout, stderr = await proc.communicate()
#     print(stdout,stderr)



# async def main():
#     command='zip - t.txt '
#     result=await cmd_run(command)
#     print(result)



# if __name__ =='__main__':
#     asyncio.run(main())
