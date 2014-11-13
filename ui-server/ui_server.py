#!/usr/bin/env python
# -*- coding: utf-8 -*-


# import json
import gflags
import os
import signal
from urlparse import urlparse
from ui_controller import UIController
import tornado.httpserver
import tornado.web


gflags.DEFINE_string("camera_server_url", "http://localhost:4999",
                     "url to camera server")

FLAGS = gflags.FLAGS


# TODO 認証をつける (http://conta.hatenablog.com/entry/2012/05/31/222940)
class AdminHandler(tornado.web.RequestHandler):

    def initialize(self, controller):
        self.controller = controller

    def get(self):
        phase, message = self.controller.get_message()
        clients = self.controller.get_clients()
        indexes = self.controller.indexes()
        for index in clients:
            if index in indexes:
                clients[index]['passphrase'] = indexes[index]
            else:
                clients[index]['passphrase'] = None
        host = self.request.host
        self.render("admin.html", host='http://%s' % host, clients=clients,
                    phase=phase, message=message)


class AdminAPIHandler(tornado.web.RequestHandler):

    def initialize(self, controller):
        self.controller = controller

    def post(self):
        request = self.get_argument("request")

        if request == "register":
            index = self.get_argument("index")
            response = self.controller.register(index)
            # self.write(json.dumps(response))
        elif request == "delete":
            index = self.get_argument("index")
            response = self.controller.delete(index)
            # self.write(json.dumps(response))
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
            self.render("ui.html", index=index, passphrase=passphrase,
                    server_url=urlparse(self.controller.control_server_url).hostname)
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


class URLHandler(tornado.web.RequestHandler):
    """indexからURLをJSONで返す.

    camera-serverで使われるよ．
    { 
        url: {string} uiへのURL.存在しない場合は空文字
    }
    """

    def initialize(self, controller):
        self.controller = controller

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin",
                        FLAGS.camera_server_url)

    def get(self, index):
        url = ""
        passphrase = self.controller.passphrase(index)   
        if passphrase:
            server_addr = "%s://%s" % (self.request.protocol, self.request.host)
            url = server_addr + "/ui/%s/%s" % (index, passphrase)
        self.write(dict(url=url))


def start_server(port=5001, control_server_url="http://localhost:5000"):
    controller = UIController(control_server_url)

    def signal_term_handler(signum, frame):
        controller.clear()
        sys.exit(0)
    signal.signal(signal.SIGTERM, signal_term_handler)

    handlers = [
        (r"/", DefaultHandler),
        (r"/admin", AdminHandler, dict(controller=controller)),
        (r"/api/admin", AdminAPIHandler, dict(controller=controller)),
        (r"/ui/([0-9a-zA-Z]+)/([0-9a-zA-Z]+)", UIHandler,
         dict(controller=controller)),
        (r"/url/([0-9a-zA-Z]+)", URLHandler, dict(controller=controller)),
    ]
    settings = dict(
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
    )
    app = tornado.web.Application(handlers, **settings)

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()
