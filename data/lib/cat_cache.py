# -*- coding: utf-8 -*-

import io
import os
import uuid
import random
import logging

import aiofiles

logger = logging.getLogger()

cache_dir = "cat_cache/"


def get_cache_list():
    return os.listdir(cache_dir)


async def save_cat(file):
    file_name = f"{uuid.uuid4()}"
    logger.info(f"Saving Cat at '{cache_dir}' name as '{file_name}'")

    try:
        async with aiofiles.open(os.path.join(cache_dir, file_name), mode='wb') as worker:
            await worker.write(file.getbuffer())

        return True
    except Exception as e:
        logger.warning(f"FAIL - {e.__class__.__name__}: {e}")
        return False


async def replace_cat(file):
    caches = get_cache_list()
    old_cat_id = await get_cat_random(raw=True)
    os.remove(os.path.join(cache_dir, caches[old_cat_id]))

    return await save_cat(file)


async def get_cat_random(raw=False):
    caches = get_cache_list()
    cat_id = random.randint(0, len(caches) - 1)

    if raw is True:
        return cat_id
    return get_cat_by_id(caches[cat_id])


def get_cat_by_id(cache_id):
    try:
        with open(os.path.join(cache_dir, cache_id), mode='rb') as worker:
            return io.BytesIO(worker.read())
    except Exception as e:
        logger.warning(f"FAIL - {e.__class__.__name__}: {e}")
        return False


def check_dir():
    logger.info(f"Testing '{cache_dir}' is online...")
    if os.path.isdir(os.path.join(cache_dir)):
        logger.info(f"'{cache_dir}' is online!")
    else:
        os.mkdir(cache_dir)
        logger.info(f"'{cache_dir}' is now online!")
