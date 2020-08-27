# -*- coding: utf-8 -*-

import os
import json
import logging

logger = logging.getLogger()


def load_filter(file_name):
    logger.info(f"Loading words from {file_name}")
    if file_name.split(".")[-1] == "txt":
        with open(f"./data/filter/{file_name}", "r", encoding="utf-8") as filter_file:
            cache = filter_file.read()

        cache = cache.replace("\n", ",")
        cache = cache.replace(" ", "").split(",")
        return cache
    else:
        logger.warning("Filter file must be [*.txt] file")
        return None


def get_filter():
    logger.info("Searching filter...")
    items = os.listdir("./data/filter/")

    filters = list()
    for item in items:
        cache = load_filter(item)
        if cache is not None:
            for tmp in cache:
                filters.append(tmp)

    logger.info("--------<< Filter Information >>--------")
    logger.info(f" - {len(filters)} words")
    logger.info(f" - Use the 'filter' command to get more information!")

    json.dump(filters, open("data/cache__filters.json", mode="w", encoding="utf-8"))
    return filters
