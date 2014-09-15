#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import gflags
import os
import ui_server


gflags.DEFINE_integer("port", 0, "port number the server listen on")
gflags.DEFINE_string("control_server_url", "http://localhost:5000",
                     "URL of control server")


def main(argv):
    argv = gflags.FLAGS(argv)

    if gflags.FLAGS.port == 0:
        port = int(os.environ.get("PORT", 5001))
    else:
        port = gflags.FLAGS.port
    ui_server.start_server(port=port,
                           control_server_url=gflags.FLAGS.control_server_url)

if __name__ == '__main__':
    main(sys.argv)
