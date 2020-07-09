# -*- coding: utf-8 -*-

import aiohttp


async def get_data(api_url: str, json_key: str):
    async def get():
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as resp:
                return await resp.json()

    cache = await get()
    return cache[json_key].replace("\\", '')
