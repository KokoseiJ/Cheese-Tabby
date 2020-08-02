# -*- coding: utf-8 -*-

import aiohttp
import logging

logger = logging.getLogger()


async def get_data(api_url: str, json_key: str, tm_out: int):
    async def get():
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=tm_out)) as session:
                async with session.get(api_url) as resp:
                    if resp.status == 200:
                        return True, await resp.json()
                    else:
                        logger.critical(f"API Server returns {resp.status} not 200!!")
                        return False, resp.status
        except Exception as e:
            logger.critical("API Server Connect Error!!")
            logger.info(f"Detail: {e}")
            return False, 400

    cache = await get()
    if cache[0] is False:
        return cache
    else:
        return cache[0], cache[1][json_key].replace("\\", '')
