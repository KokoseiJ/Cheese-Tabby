# -*- coding: utf-8 -*-

import os
import json
import logging

logger = logging.getLogger()


def read_file(file_name: str):
    logger.info(f"Loading words from {file_name}")
    if file_name.split(".")[-1] == "txt":
        with open(f"./data/filter/{file_name}", "r", encoding="utf-8") as filter_file:
            cache = filter_file.read()

        cache = cache.replace("\n", ",")
        cache = cache.replace(" ", "").split(",")
        return cache
    elif file_name.split(".")[-1] == "json":
        return None
    else:
        logger.warning("Filter file must be [*.txt] file")
        return None


def get():
    logger.info("Searching filter...")
    items = os.listdir("./data/filter/")

    filters = list()
    for item in items:
        cache = read_file(file_name=item)
        if cache is not None:
            for tmp in cache:
                filters.append(tmp)

    logger.info("--------<< Filter Information >>--------")
    logger.info(f" - {len(filters)} words")
    logger.info(f" - Use the 'filter' command to get more information!")

    json.dump(
        obj=filters,
        fp=open(
            "data/cache__filters.json",
            mode="w",
            encoding="utf-8"
        )
    )
    return filters
