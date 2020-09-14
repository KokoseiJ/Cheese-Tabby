# -*- coding: utf-8 -*-

import io
import os
import random
import logging
import hashlib

import aiofiles

from option import cache_dir

logger = logging.getLogger()


def get_cache_list():
    return os.listdir(cache_dir)


def get_size_by_id(cache_id: str):
    return os.path.getsize(os.path.join(cache_dir, cache_id))


def get_cache_size():
    items = get_cache_list()
    result = 0

    logger.info(f"Try to get size in '{cache_dir}'")
    for item in items:
        try:
            result = result + get_size_by_id(cache_id=item)
        except Exception as e:
            logger.warning(f"FAIL - {e.__class__.__name__}: {e}")

    logger.info(f"Cache Size: {result}")
    return result


async def save_img(file):
    filename = get_hash_by_byte(
        byte_data=bytes(file.getbuffer())
    )

    logger.info(f"Try to Save Image at '{cache_dir}' name as '{filename}'")

    try:
        async with aiofiles.open(os.path.join(cache_dir, filename), mode='wb') as worker:
            await worker.write(file.getbuffer())

        logging.info(f"OK! - Image Saved! '{os.path.join(cache_dir, filename)}")
        return filename
    except FileExistsError:
        logger.info("PASS - Already Cached Image!")
    except Exception as e:
        logger.warning(f"FAIL - {e.__class__.__name__}: {e}")
        return None


async def replace_img(file):
    old_cache = await get_img_random(raw=True)
    os.remove(os.path.join(cache_dir, old_cache))
    return await save_img(file=file)


async def get_img_random(raw: bool = False, return_with_cache_id: bool = False):
    caches = get_cache_list()
    try:
        random_address = random.randint(0, len(caches) - 1)
    except ValueError:
        if return_with_cache_id is True:
            return None, None
        return None

    if raw is True:
        return caches[random_address]
    else:
        if return_with_cache_id is True:
            return await get_image_by_id(cache_id=caches[random_address]), caches[random_address]
        else:
            return await get_image_by_id(cache_id=caches[random_address])


async def get_image_by_id(cache_id: str):
    try:
        async with aiofiles.open(os.path.join(cache_dir, cache_id), mode='rb') as worker:
            content = await worker.read()
            return io.BytesIO(content)
    except Exception as e:
        logger.warning(f"FAIL - {e.__class__.__name__}: {e}")
        return False


def purge_cache():
    caches = get_cache_list()
    for cache in caches:
        try:
            os.remove(os.path.join(cache_dir, cache))
            logger.info(f"'{cache}' removed")
        except Exception as e:
            logger.info(f"Fail to remove '{cache}' cause '{e.__class__.__name__}: {e}'")


async def get_hash_by_id(cache_id: str):
    image = await get_image_by_id(cache_id=cache_id)
    if image is not False:
        return get_hash_by_byte(byte_data=bytes(image.getbuffer()))
    else:
        return None


def get_hash_by_byte(byte_data: bytes):
    return hashlib.md5(byte_data).hexdigest()
