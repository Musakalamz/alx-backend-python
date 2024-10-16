#!/usr/bin/env python3
""" Measure the runtime of an Async comprehension """
from asyncio import gather
import time
async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """ Measure the runtime of 4 async comprehensions"""
    s = time.perf_counter()
    await gather(
        async_comprehension(),
        async_comprehension(),
        async_comprehension(),
        async_comprehension()
    )
    elapsed = time.perf_counter() - s
    return elapsed
