# -*- coding: utf-8 -*-

import io
import os
import uuid
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


async def save_cat(file):
    cache_id = f"{uuid.uuid4()}"
    logger.info(f"Try to Save Cat at '{cache_dir}' name as '{cache_id}'")

    try:
        async with aiofiles.open(os.path.join(cache_dir, cache_id), mode='wb') as worker:
            await worker.write(file.getbuffer())

        logging.info(f"Cat Saved! '{os.path.join(cache_dir, cache_id)}")
        return cache_id
    except Exception as e:
        logger.warning(f"FAIL - {e.__class__.__name__}: {e}")
        return None


async def replace_cat(file):
    old_cat = await get_cat_random(raw=True)
    os.remove(os.path.join(cache_dir, old_cat))
    return await save_cat(file=file)


async def get_cat_random(raw: bool = False, return_with_cat_id: bool = False):
    caches = get_cache_list()
    try:
        cat_id = random.randint(0, len(caches) - 1)
    except ValueError:
        if return_with_cat_id is True:
            return None, None
        return None

    if raw is True:
        return caches[cat_id]
    else:
        if return_with_cat_id is True:
            return await get_cat_by_id(cache_id=caches[cat_id]), caches[cat_id]
        else:
            return await get_cat_by_id(cache_id=caches[cat_id])


async def get_cat_by_id(cache_id: str):
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
    cat = await get_cat_by_id(cache_id=cache_id)
    if cat is not False:
        return get_hash_by_byte(byte_data=bytes(cat.getbuffer()))
    else:
        return None


def get_hash_by_byte(byte_data: bytes):
    return hashlib.md5(byte_data).hexdigest()


async def purge_same():
    cache_list = get_cache_list()
    cache_hash = []

    for i in cache_list:
        t = await get_hash_by_id(i)
        if t not in cache_hash:
            cache_hash.append(t)
        else:
            os.remove(os.path.join(cache_dir, i))
            logger.info(f"Duplicate cache '{i}' deleted")
