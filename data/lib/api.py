# -*- coding: utf-8 -*-

import io
import logging

import aiohttp

logger = logging.getLogger()


async def download(url: str, tm_out: int):
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=tm_out)) as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    if resp.headers['Content-Type'].startswith("image"):
                        return io.BytesIO(await resp.read())
                    else:
                        raise ValueError("This is not Image!!")
                else:
                    logger.critical(f"Web Server returns {resp.status} not 200!!")
                    return False, resp.status
    except Exception as e:
        logger.critical("Web Server Connect Error!!")
        logger.info(f"Detail-> {e.__class__.__name__}: {e}")
        return None


async def get_data(api_url: str, tm_out: int):
    async def get():
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=tm_out)) as session:
                async with session.get(api_url) as resp:
                    if resp.status == 200:
                        if resp.headers['Content-Type'].startswith("image"):
                            data = io.BytesIO(await resp.read())
                            return True, data
                        else:
                            raise ValueError("This is not Image!!")
                    else:
                        logger.critical(f"API Server returns {resp.status} not 200!!")
                        return False, resp.status
        except Exception as e:
            logger.critical("API Server Connect Error!!")
            logger.info(f"Detail-> {e.__class__.__name__}: {e}")
            return False, 400

    cache = await get()
    return cache
