# -*- coding: utf-8 -*-

import os
import hashlib


def get_name(filename: str):
    with open(os.path.join("input", filename), mode="rb") as f:
        return hashlib.md5(bytes(f.read())).hexdigest()


if __name__ == '__main__':
    if not os.path.isdir("input"):
        os.mkdir("input")
    if not os.path.isdir("output"):
        os.mkdir("output")

    for item in os.listdir(path=os.path.join("input")):
        if not item.startswith("__"):
            new_name = get_name(filename=item)
            print(f"{item} => {new_name}")

            os.rename(
                src=os.path.join("input", item),
                dst=os.path.join("output", new_name)
            )
