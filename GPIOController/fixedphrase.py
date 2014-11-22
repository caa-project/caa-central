#!/usr/bin/env python
# -*- coding: utf-8 -*-


import gflags
import subprocess
import threading

FLAGS = gflags.FLAGS

gflags.DEFINE_string("command", "aplay --quiet", "command to play wav.")
gflags.DEFINE_string("phrase_list", None, "list of path to wav files")


files = list()


def initialize():
    """Set file path."""
    with open(FLAGS.phrase_list) as f:
        for line in f.read().split("\n"):
            if line:
                files.append(line)


def say(idx_phrase):
    """Play sound using aplay."""
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
