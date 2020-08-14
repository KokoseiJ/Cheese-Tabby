# -*- coding: utf-8 -*-

import os

from option import prefix

help = None


def gen_msg(command, msg):
    if command is None or msg is None:
        return ""
    return "{{prefix}}" + f"{command} - {msg}\n"


async def main(message, client):
    help_msg = ""
    for i in os.listdir("data/command/"):
        if not i.startswith("__"):
            i = i.split('.')[0]

            t = __import__(f"data.command.{i}")
            help_msg += gen_msg(i, getattr(getattr(t.command, i), "help"))

    help_msg += "\n" + gen_msg("help", "Show this message")

    help_msg = help_msg.replace("{{prefix}}", prefix)
    help_msg = help_msg.replace("{{bot}}", str(client.user))
    await message.channel.send("```\n" + help_msg + "\n```")

    return
