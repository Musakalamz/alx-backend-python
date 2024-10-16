#!/usr/bin/env python3
""" Async Comprehension """
import asyncio
from typing import List
async_generator = __import__('0-async_generator').async_generator


async def async_comprehension() -> List[float]:
    """ Returns List of random floats [0, 10) generated after 10 seconds """
    return [i async for i in async_generator()]
