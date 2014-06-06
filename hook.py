#!/usr/bin/env python
import os
import sys
import subprocess


PRINTER = 'Canon_CP900_2'
# PRINTER = 'Brother_HL_2270DW_series'
# (`lpstat -p`)

MEDIA = 'Postcard(4x6in)'  # selphy


class BorkException(Exception):
    """Urgh!"""


def run(cmd):
    print "RUN:", cmd
    r = subprocess.call(cmd, shell=True)
    if not r == 0:
        raise BorkException()


def handle_hook(action, argument=None):
    print 'action:', action
    if action == 'download':
        run("lpr -P {} -o media='{}' {}".format(PRINTER, MEDIA, argument))


if __name__ == '__main__':
    action = os.environ.get('ACTION')
    argument = os.environ.get('ARGUMENT', None)

    handle_hook(action, argument)

    sys.exit(0)
