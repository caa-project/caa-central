#!/usr/bin/env python
# -*- coding: utf-8 -*-


import control_proxy
import json
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


# TODO 認証をつける (http://conta.hatenablog.com/entry/2012/05/31/222940)
class AdminHandler(tornado.web.RequestHandler):

    pass_dict = dict()  # index: passphrase

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
                UIHandler.add_pass(index, passphrase)
                AdminHandler.pass_dict[index] = passphrase
                self.write("Registered "+index+":"+passphrase)
            except Exception as e:
                msg = "Error: "+e.message
                print msg
                self.write(msg)
            except:
                self.write("Unknown error")
        elif request == "delete":
            try:
                index = self.get_argument("index")
                response = self.control_proxy.delete(index)
                passphrase = AdminHandler.pass_dict.pop(index)
                UIHandler.remove_pass(index, passphrase)
                self.write("Deleted "+json.dumps(response))
            except Exception as e:
                msg = "Error: "+e.message
                print msg
                self.write(msg)
            except:
                self.write("Unknown error")
        else:
            self.write("wow")


class UIHandler(tornado.web.RequestHandler):
    """index:passphraseに対応したページを提供するよ
    このページを見ている時点で認証できていることにするので，特に認証しないよ．
    """

    pass_set = set()    # 今見せている(index, passphrase)

    def get(self, index, passphrase):
        if (index, passphrase) in UIHandler.pass_set:
            # TODO render html
            self.write("Hello %s" % (index))
        else:
            self.write_error(403)

    @classmethod
    def add_pass(cls, index, passphrase):
        cls.pass_set.add((index, passphrase))

    @classmethod
    def remove_pass(cls, index, passphrase):
        cls.pass_set.remove((index, passphrase))


class DefaultHandler(tornado.web.RequestHandler):
    """<h1>It works!</h1>"""

    def get(self):
        self.render("index.html")


def start_server(port=5001, control_server_url="http://localhost:5000"):
    handlers = [
        (r"/", DefaultHandler),
        (r"/admin", AdminHandler, dict(control_server_url=control_server_url)),
        (r"/ui/([0-9]+)/([0-9a-zA-Z]+)", UIHandler),
    ]
    settings = dict(
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
    )
    app = tornado.web.Application(handlers, **settings)

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()
