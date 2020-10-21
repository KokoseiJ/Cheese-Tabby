# -*- coding: utf-8 -*-

import json
import logging

logger = logging.getLogger()


class Token:
    def __init__(self, file_name: str, service: str):
        self.name = file_name
        self.service = service

    def get_token(self):
        logger.info("Loading Token...")
        try:
            logger.info("OK! - File exists")
            loaded_token = json.load(open(self.name))['token']

            if self.service == "Discord":
                logger.info("Token length check...")
                if len(loaded_token) == 59:
                    logger.info("OK! - Token is Ready!")
                else:
                    logger.critical("FAIL - Invalid token detected")
                    loaded_token = "#"
        except FileNotFoundError:
            logger.critical("Token File Not Found")
            loaded_token = "#"

        return loaded_token

    def update_token(self, new_token: str):
        try:
            logger.info("Updating Token...")
            with open(self.name, "w", encoding="utf8") as f:
                f.write(json.dumps({"token": new_token}, indent=4))
            logger.info("OK! - Token is Updated!")
        except Exception as e:
            logger.critical(f"FAIL - {e}")

    def reset_token(self):
        try:
            logger.info("Reset Token...")
            with open(self.name, "w", encoding="utf8") as f:
                f.write(json.dumps({"token": "#"}, indent=4))
            logger.info("OK! - Token is now the default value")
        except Exception as e:
            logger.critical(f"FAIL - {e}")
