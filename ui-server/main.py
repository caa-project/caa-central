#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import gflags
import os
import ui_server


gflags.DEFINE_integer("port", 0, "port number the server listen on")
gflags.DEFINE_string("control_server_url", "http://localhost:5000",
                     "URL of control server")
gflags.DEFINE_boolean("enable_debug_ui", False,
                      "Enable debug ui: ui/9999/debug")
FLAGS = gflags.FLAGS


def main(argv):
    argv = gflags.FLAGS(argv)

    if FLAGS.port == 0:
        port = int(os.environ.get("PORT", 5001))
    else:
        port = FLAGS.port

    debug_index_pass = None
    if FLAGS.enable_debug_ui:
        debug_index_pass = ("9999", "debug")

    ui_server.start_server(port=port,
                           control_server_url=gflags.FLAGS.control_server_url,
                           debug_index_pass=debug_index_pass)

if __name__ == '__main__':
    main(sys.argv)
