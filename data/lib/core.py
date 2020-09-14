# -*- coding: utf-8 -*-

import io
import logging

import aiohttp

import option
from data.lib import img_cache

logger = logging.getLogger()


async def save_cache(image: bytes):
    if option.cache_limit > len(img_cache.get_cache_list()):
        logger.info("Adding Cat to 'cat_cache'...")

        await img_cache.save_img(image)
    else:
        logger.info("Cache is full!")

        if option.replace_on_limit is True:
            logger.info("Replace option is enabled!")
            logger.info("Adding Cat to 'cat_cache'...")
            await img_cache.replace_img(image)
        pass


async def get_from_api():
    async def get():
        try:
            timeout = int(option.timeout)
        except ValueError:
            logger.critical("Warning! Timeout option is not integer")
            logger.critical("Set timeout to default value [ 3 ] ")
            timeout = 3

        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as session:
                async with session.get(option.api_url) as resp:
                    if resp.status == 200:
                        if resp.headers['Content-Type'].startswith("image"):
                            data = io.BytesIO(await resp.read())
                            return 200, data
                        else:
                            logger.critical("Header Said: This is not Image!!")
                            return 200, None
                    else:
                        logger.critical(f"API Server returns {resp.status} not 200!!")
                        return resp.status, None

        except Exception as e:
            logger.critical("API Server Connect Error!!")
            logger.info(f"Detail-> {e.__class__.__name__}: {e}")
            return -1, None

    api_status, api_image = await get()

    if api_status == 200:
        if api_image is None:
            return get_from_cache(
                msg="Header Said: This is not Image!!"
            )

        cache_id = img_cache.get_hash_by_byte(
            byte_data=bytes(api_image.getbuffer())
        )
        return api_image, cache_id, "from api"
    elif api_status == -1:
        return await get_from_cache(
            msg="Fail to Connect to API Server..."
        )
    else:
        return await get_from_cache(
            msg=f"API Server return status code {api_status} not 200"
        )


async def get_from_cache(msg: str = None):
    if len(img_cache.get_cache_list()) == 0:
        logging.warning("Cache Directory is EMPTY!")
        logging.warning("Send Error Message!")

        if msg is None:
            msg = "**Cache is EMPTY!!!**\n" \
                  "- add image at cache directory!"

        return None, None, msg
    else:
        image, cache_id = await img_cache.get_img_random(
            return_with_cache_id=True
        )
        return image, cache_id, msg


async def work():
    if option.use_cache_only is True:
        return await get_from_cache()
    else:
        return await get_from_api()
