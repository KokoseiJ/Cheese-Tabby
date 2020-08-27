# -*- coding: utf-8 -*-

# API Option
api_url = "https://cataas.com/cat?width=300"
timeout = 3

# Cache Option
cache_limit = 100000
replace_on_limit = True
cache_dir = "img_cache/"

# Bot Option
prefix = "=="
default_permission = 35904
use_Auto_shard = True


# Bot Presence
class presence:
    # [online / idle / dnd]
    status = "idle"

    # [playing / streaming / listening / watching]
    activity = "watching"

    name = "Cat"


# Offline Mode
use_cache_only = False
