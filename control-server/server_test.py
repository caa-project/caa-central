# -*- coding: utf-8 -*-

from server import *
from tornado.testing import AsyncHTTPTestCase
import tornado.web
import unittest
import websocket
import json


class CAAControlServerTest(AsyncHTTPTestCase):

    def get_app(self):
        """@Override"""
        ClientContainer.instance().set_num_max(3)

        return tornado.web.Application([
            (r"/robo/register", RobotRegisterHandler),
            (r"/robo/delete", RobotDeleteHandler),
            (r"/robo/([0-9]+)", RobotSocketHandler),
            (r"/user/register", UserRegisterHandler),
            (r"/user/delete", UserDeleteHandler),
            (r"/user/([0-9]+)/([0-9a-zA-Z]+)", UserSocketHandler),
            (r"/clients", ClientsHandler)
        ])

    def tearDown(self):
        """@Override"""
        ClientContainer._instance = ClientContainer()

    def test_register(self):
        response0 = json.loads(self.fetch(r"/robo/register?index=1024").body)
        self.assertTrue(response0['succeeded'])
        self.assertEqual(response0['index'], '1024')

        response1 = json.loads(
                self.fetch(r"/user/register?index=1024&passphrase=hogehoge").body)
        self.assertTrue(response1['succeeded'])

    def test_delete(self):
        response0 = json.loads(self.fetch(r"/robo/register?index=1024").body)
        self.assertTrue(response0['succeeded'])
        self.assertEqual(response0['index'], '1024')

        response1 = json.loads(
                self.fetch(r"/user/register?index=1024&passphrase=hogehoge").body)
        self.assertTrue(response1['succeeded'])

        response2 = json.loads(self.fetch(r"/user/delete?index=1024").body)
        self.assertTrue(response2['succeeded'])

        response3 = json.loads(self.fetch(r"/robo/delete?index=1024").body)
        self.assertTrue(response3['succeeded'])

if __name__ == '__main__':
    unittest.main()
