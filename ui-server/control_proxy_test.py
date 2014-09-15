#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from control_proxy import ControlProxy


class ControlServerProxyTest(unittest.TestCase):

    def setUp(self):
        self.control_server_url = "http://localhost:5000"

    def test_get_url(self):
        proxy = ControlProxy(self.control_server_url)

        self.assertEqual("http://localhost:5000/hoge", proxy._get_url("hoge"))
        self.assertEqual("http://localhost:5000/hoge/foo/bar",
                         proxy._get_url("hoge", "foo", "bar"))
        self.assertEqual("http://localhost:5000/hoge/foo/bar",
                         proxy._get_url("hoge/foo/bar"))

    def test_fetch_json(self):
        proxy = ControlProxy("http://api.openweathermap.org")

        # Fetch Tokyo weather
        response = proxy._fetch_json("/data/2.5/weather?q=Tokyo,jp")
        self.assertEqual("Tokyo", response["name"])

if __name__ == '__main__':
    unittest.main()
