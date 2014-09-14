#!/usr/bin/env python
# -*- coding: utf-8 -*-

from server import Auth
from server import DumpHandler
from server import DeleteHandler
from server import OperationHandler
from server import RegisterHandler
from server import RobotHandler
from tornado.testing import AsyncHTTPTestCase
import tornado.web
import unittest
import websocket


class CAAControlServerTest(AsyncHTTPTestCase):

    def get_app(self):
        """@Override"""
        self.url_base = "http://hoge.com/"

        Auth.instance().set_num_max(3)

        return tornado.web.Application([
            (r"/register/([0-9]+)/([0-9a-zA-Z]+)", RegisterHandler),
            (r"/dump", DumpHandler),
            (r"/delete/([0-9]+)", DeleteHandler),
            (r"/operation/([0-9]+)/([0-9a-zA-Z]+)", OperationHandler),
            (r"/robo/([0-9]+)", RobotHandler),
        ])

    def tearDown(self):
        """@Override"""
        Auth.instance()._clear()
        super(AsyncHTTPTestCase, self).tearDown()

    def testAuth(self):
        auth = Auth.instance()

        self.assertEqual(3, auth.num_max())

        auth.register("1", "abc123")
        self.assertEqual("abc123", auth._pass_dict["1"])

        auth.register("300", "aaa111")
        self.assertRaises(Exception,
                          auth.register, ("300", "aaa11"))
        auth.register("2", "bbb222")
        self.assertRaises(Exception,
                          auth.register, ("111", "aaa"))
        auth.delete("300")
        self.assertRaises(Exception,
                          auth.delete, ("300"))

        self.assertTrue(auth.auth("1", "abc123"))
        self.assertFalse(auth.auth("1", "abc"))

        self.assertEqual("1: abc123\n2: bbb222\n", auth.dump())

    def testCreateAndKill(self):
        # Create
        response = self.fetch(r"/register/1/abcd1234")
        self.assertIn("Registered index '1'", response.body)

        response = self.fetch(r"/register/3/efgh3456")
        self.assertIn("Registered index '3'", response.body)

        response = self.fetch(r"/register/100/efgh3456")
        self.assertIn("Registered index '100'", response.body)

        # Kill
        response = self.fetch(r"/delete/3")
        self.assertIn("Deleted index '3'", response.body)

        # TODO エラーのテスト: 数の上限を超えてregister, 重複したindexでのcreate,
        # 存在しないindexでのdelete,

    # TODO wsの接続ができない？？？
    # def testRobotHandler(self):
    #     """ Read here
    #     http://www.giantflyingsaucer.com/blog/?p=4602
    #     """
    #     url = self.get_url("/robo/1").replace("http", "ws")
    #     ws = websocket.create_connection(url)
    #     RobotHandler.write_message_to("1", "hoge")
    #     result = ws.recv()
    #     self.assertEqual("hoge", result)
    #     ws.close()


if __name__ == '__main__':
    unittest.main()
