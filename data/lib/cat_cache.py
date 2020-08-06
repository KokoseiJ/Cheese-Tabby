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
    logger.info(f"Try to Save Cat at '{cache_dir}' name as '{file_name}'")

    try:
        async with aiofiles.open(os.path.join(cache_dir, file_name), mode='wb') as worker:
            await worker.write(file.getbuffer())
            
        logging.info(f"Cat Saved! '{os.path.join(cache_dir, file_name)}")
        return True
    except Exception as e:
        logger.warning(f"FAIL - {e.__class__.__name__}: {e}")
        return False


async def replace_cat(file):
    old_cat = await get_cat_random(raw=True)
    os.remove(os.path.join(cache_dir, old_cat))

    return await save_cat(file)


async def get_cat_random(raw=False):
    caches = get_cache_list()
    cat_id = random.randint(0, len(caches) - 1)

    if raw is True:
        return caches[cat_id]
    return get_cat_by_id(caches[cat_id])


def get_cat_by_id(cache_id):
    try:
        with open(os.path.join(cache_dir, cache_id), mode='rb') as worker:
            return io.BytesIO(worker.read())
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


def check_dir():
    logger.info(f"Testing '{cache_dir}' is online...")
    if os.path.isdir(os.path.join(cache_dir)):
        logger.info(f"'{cache_dir}' is online!")
    else:
        os.mkdir(cache_dir)
        logger.info(f"'{cache_dir}' is now online!")
