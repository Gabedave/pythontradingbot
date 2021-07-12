import subprocess
import os
import sys
from multiprocessing import Process
from iqoptionbot.starter import start

def execute_gen(your_command):
    process = subprocess.Popen(your_command, stdout=subprocess.PIPE, shell=True)
    for line in iter(process.stdout.readline, b''):
        # f.write(line)
        yield line

# from contextlib import redirect_stdout
# import io

# def execute_multi(func):
#     # sys.stdout = open("test.log",'w')      # str(os.getpid()) + ".out", "w")
#     starter = Process(target=func)
#     starter.start()
#     f = io.StringIO()
#     with redirect_stdout(f):
#         with open('test.log', 'wb') as g:
#             for line in iter(f.getvalue()):
#                 print('check')
#                 g.write(line)
#     starter.close()

# def iter_over_async(ait, loop):
#     ait = ait.__aiter__()
#     async def get_next():
#         try:
#             obj = await ait.__anext__()# s = f.getvalue()
#             return False, obj
#         except StopAsyncIteration:
#             return True, None
#     while True:
#         done, obj = loop.run_until_complete(get_next())
#         if done:
#             break
#         yield obj

# def sync_ticker_generator(command):
#     loop = asyncio.get_event_loop()
#     async_gen = execute_gen(command)
#     sync_gen = iter_over_async(async_gen, loop)
#     return sync_gen

if __name__=='__main__':
    gen = execute_gen(['PYTHONPATH=.','python','iqoptionbot/starter.py'])
    while True:
        print(next(gen))

