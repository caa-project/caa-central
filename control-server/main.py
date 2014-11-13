#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import gflags
import os
import server


gflags.DEFINE_integer("num_robots", 1, "number of robots", lower_bound=0)
gflags.DEFINE_integer("port", 0, "port number the server listen on")


def main(argv):
    argv = gflags.FLAGS(argv)

    if gflags.FLAGS.port == 0: # default value
        port = int(os.environ.get("PORT", 5000))
    else:
        port = gflags.FLAGS.port
    server.start_server(port=port, num_robots_max=gflags.FLAGS.num_robots)

if __name__ == '__main__':
    main(sys.argv)
