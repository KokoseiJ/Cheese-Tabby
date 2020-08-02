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
        logger.info(f"FAIL - [{option_file}] not found, please copy from option_example")
        sys.exit(-1)

    return option


def update_option(new_option):
    logger.info(f"Updating Option...")
    try:
        with open(option_file, "w", encoding="utf-8") as option_f:
            option_f.write(json.dumps(new_option))
        logger.info("OK! - Option is Updated")
        return True
    except Exception as e:
        logger.info(f"FAIL - {e}")
        return False
