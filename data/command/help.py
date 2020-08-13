# -*- coding: utf-8 -*-

from option import prefix


async def main(message, client):
    with open("help_msg.txt", mode='r') as worker:
        help_msg = worker.read()

    help_msg = help_msg.replace("{{prefix}}", prefix)
    help_msg = help_msg.replace("{{bot}}", str(client.user))
    await message.channel.send("```\n" + help_msg + "\n```")

    return
