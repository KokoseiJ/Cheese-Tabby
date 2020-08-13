# -*- coding: utf-8 -*-

import logging

import option
from data.lib import api, cat_cache


logger = logging.getLogger()


async def get():
    try:
        tm_out = int(option.timeout)
    except ValueError:
        logger.critical("Warning! Timeout option is not integer")
        logger.info("Set timeout to default value [3] ")
        tm_out = 3

    cat_worker = await api.get_data(api_url=option.api_url,
                                    tm_out=tm_out)

    if cat_worker[0] is False:
        logging.info("Try to use Cat Cache...")
        if len(cat_cache.get_cache_list()) == 0:
            logging.warning("'cat_cache' is EMPTY!")
            logging.warning("Send Error Message!")
            return f"**WARNING! API SERVER ERROR!**\n - {cat_worker[1]}"
        else:
            return await cat_cache.get_cat_random()
    elif cat_worker[0] is True:
        if option.cache_limit > len(cat_cache.get_cache_list()):
            logger.info("Adding Cat to 'cat_cache'...")
            await cat_cache.save_cat(cat_worker[1])
        else:
            logger.info("Cache is full!")
            if option.replace_on_limit is True:
                logger.info("Replace option is enabled!")
                logger.info("Adding Cat to 'cat_cache'...")
                await cat_cache.replace_cat(cat_worker[1])
            pass

        return cat_worker[1]