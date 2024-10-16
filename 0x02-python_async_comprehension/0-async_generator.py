#!/usr/bin/env python3
""" Generate asynchronous random numbers """
import asyncio
import random
from typing import Generator


async def async_generator() -> Generator[float, None, None]:
    """ Generates random numbers [0.0, 10.0) and sleeps for 1 second """
    for _ in range(10):
        await asyncio.sleep(1)
        yield random.random()
