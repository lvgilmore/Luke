#! /usr/bin/python2.7

from RoryCommiter import RoryCommiter

COMMITERS = {
    "Rory": {
        "handler": RoryCommiter,
    },
}

__all__ = ["RoryCommiter", "COMMITERS"]