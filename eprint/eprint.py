#!/bin/python

#error print. prints to stderr!

#Stolen from: https://stackoverflow.com/questions/5574702/how-to-print-to-stderr-in-python

from __future__ import print_function
import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
