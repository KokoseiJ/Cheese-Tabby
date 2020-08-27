# -*- coding: utf-8 -*-

import logging

from data.lib import api, img_cache
import option

logger = logging.getLogger()


async def get():
    try:
        tm_out = int(option.timeout)
    except ValueError:
        logger.critical("Warning! Timeout option is not integer")
        logger.info("Set timeout to default value [3] ")
        tm_out = 3

    if option.use_cache_only is False:
        cat_worker = await api.get_image(
            api_url=option.api_url,
            tm_out=tm_out
        )

        if cat_worker[0] is False:
            logging.info("Try to use image cache...")
            if len(img_cache.get_cache_list()) == 0:
                logging.warning("Cache Directory is EMPTY!")
                logging.warning("Send Error Message!")
                return f"**WARNING! API SERVER ERROR!**\n - {cat_worker[1]}"
            else:
                return await img_cache.get_cat_random()
        elif cat_worker[0] is True:
            if option.cache_limit > len(img_cache.get_cache_list()):
                logger.info("Adding Cat to 'cat_cache'...")
                await img_cache.save_cat(cat_worker[1])
            else:
                logger.info("Cache is full!")
                if option.replace_on_limit is True:
                    logger.info("Replace option is enabled!")
                    logger.info("Adding Cat to 'cat_cache'...")
                    await img_cache.replace_cat(cat_worker[1])
                pass

            return cat_worker[1]
    else:
        if len(img_cache.get_cache_list()) == 0:
            logging.warning("Cache Directory is EMPTY!")
            logging.warning("Send Error Message!")

            return "**Cache is EMPTY!!!**\n" \
                   "add image at cache directory or turn off the use_cache_only mode"
        else:
            return await img_cache.get_cat_random()

