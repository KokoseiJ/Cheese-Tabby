# -*- coding: utf-8 -*-

async def check(message, client):
    app = await client.application_info()
    if app.owner.id == message.author.id:
        return True
    else:
        if app.team is None:
            return False

        for tm in app.team.members:
            if message.author.id == tm.id:
                return True

        return False
