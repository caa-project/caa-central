#!/usr/bin/env python
# -*- coding: utf-8 -*-


from ui_controller import UIController
import json
import os
import tornado.httpserver
import tornado.web


# TODO 認証をつける (http://conta.hatenablog.com/entry/2012/05/31/222940)
class AdminHandler(tornado.web.RequestHandler):

    def initialize(self, host, controller):
        self.host = host
        self.controller = controller

    def get(self):
        phase, message = self.controller.get_message()
        kwargs = {
                "host" : self.host,
                "indexes": [item for item in self.controller.indexes()],
                "phase": phase,
                "message": message
            }
        self.render("admin.html", **kwargs)


class AdminAPIHandler(tornado.web.RequestHandler):

    def initialize(self, controller):
        self.controller = controller

    def post(self):
        request = self.get_argument("request")

        if request == "register":
            index = self.get_argument("index")
            response = self.controller.register(index)
            #self.write(json.dumps(response))
        elif request == "delete":
            index = self.get_argument("index")
            response = self.controller.delete(index)
            #self.write(json.dumps(response))
        else:
            self.set_status(400)
        self.redirect('/admin')


class UIHandler(tornado.web.RequestHandler):
    """index:passphraseに対応したページを提供するよ
    このページを見ている時点で認証できていることにするので，特に認証しないよ．
    """

    pass_set = set()    # 今見せている(index, passphrase)

    def initialize(self, controller):
        self.controller = controller

    def get(self, index, passphrase):
        if self.controller.auth(index, passphrase):
            self.render("ui.html", index=index)
        else:
            self.set_status(403)
            #self.write_error(403)

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
    controller = UIController(control_server_url)
    handlers = [
        (r"/", DefaultHandler),
        (r"/admin", AdminHandler, dict(host='http://localhost:5001', controller=controller)),
        (r"/api/admin", AdminAPIHandler, dict(controller=controller)),
        (r"/ui/([0-9]+)/([0-9a-zA-Z]+)", UIHandler, dict(controller = controller)),
    ]
    settings = dict(
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
    )
    app = tornado.web.Application(handlers, **settings)

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()
