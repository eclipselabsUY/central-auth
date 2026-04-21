from concurrent.futures import ThreadPoolExecutor
import asyncio

_executor = ThreadPoolExecutor(max_workers=4)


async def run_cpu_bound(func, *args):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(_executor, func, *args)
