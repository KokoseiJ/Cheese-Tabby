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
        print("CatBOT Option File is Missing!")
        logger.info(" - Download: https://github.com/chick0/CatBOT/blob/master/option.json")
        sys.exit(-1)

    return option
