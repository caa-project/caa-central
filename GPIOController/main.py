#! /usr/bin/python
# -*- coding: utf-8 -*-

import gflags
import sys
import RPi.GPIO as GPIO
import socket_client
import time

FLAGS = gflags.FLAGS

gflags.DEFINE_string("server", None, "e.g. ws://hogehoge:5000/control")


def main(argv):
    argv = gflags.FLAGS(argv)

    socket_client.init_safety()

    while True:
        try:
            ws = socket_client.get_websocket(FLAGS.server)
            ws.run_forever()
            # 再接続の試行までのインターバル
            time.sleep(1)
        except KeyboardInterrupt:
            GPIO.cleanup()
            break
        except:
            time.sleep(1)


if __name__ == '__main__':
    main(sys.argv)
