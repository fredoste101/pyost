#!/bin/python

from __future__ import print_function
import sys

def eprint(*args, **kwargs):
    """
        Prints message to stderr 
        Stolen from https://stackoverflow.com/questions/5574702/how-to-print-to-stderr-in-python
    """

    print(*args, file=sys.stderr, **kwargs)
