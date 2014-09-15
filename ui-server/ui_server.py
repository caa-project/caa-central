#!/usr/bin/env python
# -*- coding: utf-8 -*-


import control_proxy
import os
import random
import tornado.httpserver
import tornado.web


class PassGenerator():
    """Generate passphrase"""

    def __init__(self, charset="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRST\
UVWXYZ0123456789"):
        self.charset = charset

    def generate(self, length=64):
        passphrase = ""
        for i in range(length):
            passphrase += random.choice(self.charset)
        return passphrase


# TODO 認証をつける
class AdminHandler(tornado.web.RequestHandler):

    def initialize(self, control_server_url):
        self.control_server_url = control_server_url
        self.control_proxy = control_proxy.ControlProxy(control_server_url)
        self.pass_generator = PassGenerator()

    def get(self):
        self.render("admin.html")

    def post(self):
        request = self.get_argument("request")

        if request == "register":
            index = self.get_argument("index")
            passphrase = self.pass_generator.generate()
            try:
                response = self.control_proxy.register(index, passphrase)
                self.write(response[index]+":"+passphrase)
            except Exception as e:
                print e.message
                self.write(e.message)
        elif request == "delete":
            try:
                index = self.get_argument("index")
                response = self.control_proxy.delete(index)
                self.write(response[index])
            except Exception as e:
                print e.message
                self.write(e.message)
        else:
            self.write("wow")


# TODO 詳細を決める
class UIHandler(tornado.web.RequestHandler):

    def get(self, index):
        self.write("Hello %s" % index)


class DefaultHandler(tornado.web.RequestHandler):
    """<h1>It works!</h1>"""

    def get(self):
        self.render("index.html")


def start_server(port=5001, control_server_url="http://localhost:5000"):
    handlers = [
        (r"/", DefaultHandler),
        (r"/admin", AdminHandler, dict(control_server_url=control_server_url)),
        (r"/ui/([0-9]+)", UIHandler),
    ]
    settings = dict(
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
    )
    app = tornado.web.Application(handlers, **settings)

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()
