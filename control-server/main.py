#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import server


def main():
    port = int(os.environ.get("PORT", 5000))
    server.start_server(port, 3)

if __name__ == '__main__':
    main()
