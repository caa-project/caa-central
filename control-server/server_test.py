#!/usr/bin/env python
# -*- coding: utf-8 -*-

from server import Constants
from server import CreateHandler
from server import DumpHandler
from server import KillHandler
from server import OperationHandler
from server import RobotHandler
from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application
import unittest


class CAAControlServerTest(AsyncHTTPTestCase):

    def get_app(self):
        self.url_base = "http://hoge.com/"
        Constants.NUM_ROBOTS_MAX = 3

        return Application([
            (r"/create/([0-9]+)/([0-9a-zA-Z]+)", CreateHandler),
            (r"/dump", DumpHandler),
            (r"/kill/([0-9]+)", KillHandler),
            (r"/operation/([0-9]+)/([0-9a-zA-Z]+)", OperationHandler),
            (r"/robo/([0-9]+)", RobotHandler),
        ])

    def testCreateAndKill(self):
        # Create
        response = self.fetch(r"/create/1/abcd1234")
        self.assertIn("Created index '1'", response.body)

        response = self.fetch(r"/create/3/efgh3456")
        self.assertIn("Created index '3'", response.body)

        response = self.fetch(r"/create/100/efgh3456")
        self.assertIn("Created index '100'", response.body)

        # Kill
        response = self.fetch(r"/kill/3")
        self.assertIn("Killed index '3'", response.body)

        # TODO エラーのテスト: 数の上限を超えてcreate, 重複したindexでのcreate,
        # 存在しないindexでのkill,


if __name__ == '__main__':
    unittest.main()
