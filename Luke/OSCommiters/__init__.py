#! /usr/bin/python2.7

# kick this shit to another file
from RoryCommiter import RoryCommiter

COMMITERS = {
    "Linux": {
        "handler": RoryCommiter,
    },
}

__all__ = ["RoryCommiter", "COMMITERS"]