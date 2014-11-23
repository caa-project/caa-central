#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Play sound listed in a file.

Play comamnd is given in arguments.
Example:
for Linux
  fixedphrase.py --phrase_list=phrases.txt --command="aplay --quiet"
for Macintosh
  fixedphrase.py --phrase_list=phrases.txt --command="afplay"
"""


import gflags
import subprocess
import threading

FLAGS = gflags.FLAGS

gflags.DEFINE_string("command", "aplay --quiet", "command to play wav.")
gflags.DEFINE_string("phrase_list", None, "list of path to wav files")


files = list()  # path to wav files


def initialize():
    """Set file path.

    Call me BEFORE using say.
    """
    with open(FLAGS.phrase_list) as f:
        for line in f.read().split("\n"):
            if line:
                files.append(line)


def say(idx_phrase):
    """Play sound using FLAGS.commad."""
    path = files[idx_phrase]
    cmd = FLAGS.command + " " + path
    proc = subprocess.Popen(cmd, shell=True)

    def target():
        proc.wait()

    thread = threading.Thread(target=target)
    thread.start()


if __name__ == '__main__':
    import sys
    import time
    argv = gflags.FLAGS(sys.argv)
    initialize()
    say(1)
    time.sleep(1)
