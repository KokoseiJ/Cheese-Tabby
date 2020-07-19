# -*- coding: utf-8 -*-

import aiohttp


async def get_data(api_url: str, json_key: str, tm_out: int):
    async def get():
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=tm_out)) as session:
            async with session.get(api_url) as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    return None

    cache = await get()
    if cache is None:
        return None
    else:
        return cache[json_key].replace("\\", '')
