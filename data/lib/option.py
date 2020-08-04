# -*- coding: utf-8 -*-

import sys
import json
import logging

logger = logging.getLogger()
option_file = "option.json"


def get_option():
    logger.info(f"Loading Option from [{option_file}]")
    try:
        option = json.load(open(option_file))
        logger.info("OK! - Option is loaded")
    except FileNotFoundError:
        logger.info(f"Fail to load CatBOT {option_file}...")
        logger.info(" - PLZ Download again")
        logger.info(" - Download: https://github.com/chick0/CatBOT")
        sys.exit(-1)

    return option
