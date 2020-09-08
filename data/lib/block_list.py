# -*- coding: utf-8 -*-

import os
import json
import logging

from string import digits, punctuation, whitespace

logger = logging.getLogger()


def read_file(file_name: str):
    logger.info(f"Loading words from {file_name}")
    if file_name.split(".")[-1] == "json":
        return json.load(open(f"./data/block_words/{file_name}", "r", encoding="utf-8"))
    else:
        logger.warning("Filter file must be [*.txt] file")
        return None


def get():
    logger.info("Searching filter...")
    items = os.listdir("./data/block_words/")

    block_list = list()
    for item in items:
        cache = read_file(file_name=item)
        if cache is not None:
            for tmp in cache:
                block_list.append(tmp)

    logger.info("Add Number to block words...")
    for d in digits:
        block_list.append(d)

    logger.info("Add Punctuation to block words...")
    for p in punctuation:
        block_list.append(p)

    logger.info("Add Whitespace to block words...")
    for w in whitespace:
        block_list.append(w)

    logger.info("--------<< Block Words Information >>---")
    logger.info(f" - {len(block_list)} words")
    logger.info("----------------------------------------")

    json.dump(
        obj=block_list,
        fp=open(
            "data/cache__block_words.json",
            mode="w",
            encoding="utf-8"
        )
    )
    return block_list
