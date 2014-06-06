#!/usr/bin/env python
import os
import sys
import time
from datetime import datetime
import subprocess


HERE = os.path.dirname(__file__)
HOOKSCRIPT = os.path.join(HERE, "hook.py")


LOCK_FILE = "/tmp/what.lock"
LOCK_DURATION = 60  # seconds


class BorkException(Exception):
    """Urgh!"""


def run(cmd, ignore_errors=False):
    r = subprocess.call(cmd, shell=True)
    if not r == 0 and not ignore_errors:
        raise BorkException()


def grab_mutex():
    """
    Lock the booth by setting a modification timestamp on the lock file.
    """

    def read_file_age(path):
        if not os.path.isfile(path):
            return None
        with open(path, 'r') as f:
            ts = int(f.readline())
            return int(time.time()) - ts

    def set_file_age(path):
        with open(path, 'w') as f:
            now = int(time.time())
            f.write('{}\n'.format(now))

    try:
        age = read_file_age(LOCK_FILE)
    except Exception, e:
        print e, e.__class__
        raise Exception('failed to lock')
    if age and age <= LOCK_DURATION:
        return False
    else:
        # set.
        set_file_age(LOCK_FILE)
        return True


def countdown():
    for word in ['three', 'two', 'one']:
        run('say {}'.format(word))
        time.sleep(1)


def booth():
    print 'boothing.'

    ts = datetime.utcnow().strftime('%Y%m%d-%H%M%S')
    filename = 'booth-{}.jpg'.format(ts)

    # check mutex.
    if not grab_mutex():
        print 'sorry, someone else is boothing.'
        sys.exit(1)

    # kill PTPCamera
    run('killall PTPCamera 2> /dev/null', ignore_errors=True)

    # play countdown sample
    countdown()

    # run gphoto
    print 'gphoto'
    run('gphoto2 --capture-image-and-download --hook-script {hookscript} --filename {filename}'.format(
        hookscript=HOOKSCRIPT, filename=filename
        ))

    # say something
    print 'done!'


if __name__ == '__main__':
    booth()
