#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import ui_server


def main(argv):
    port = int(os.environ.get("PORT", 5000))
    control_server_url = 'http://benijake-caa-control-server.herokuapp.com'
    ui_server.start_server(port=port, control_server_url=control_server_url)

if __name__ == '__main__':
    main(sys.argv)
