# -*- coding: utf-8 -*-

from container import ClientContainer

import tornado.httpserver
import tornado.web
import tornado.websocket
import json
import logging

logger = logging.getLogger("caa.control.api")

def exception(handler, error):
    logger.exception(e)
    handler.write(json.dumps({
        'succeeded': False,
        'message': str(error)
    }))

class RobotRegisterHandler(tornado.web.RequestHandler):

    def get(self):
        container = ClientContainer.instance()
        try:
            index = container.add()
            self.write(json.dumps({
                'succeeded': True,
                'index': index
            }))
        except Exception as e:
            exception(self, e)


class RobotDeleteHandler(tornado.web.RequestHandler):

    def get(self, index):
        container = ClientContainer.instance()
        container.delete_robot_ws(index)


class RobotSocketHandler(tornado.websocket.WebSocketHandler):

    def check_origin(self, origin):
        """@Override"""
        return True

    def open(self, index):
        """@Override"""
        self.index = index
        container = ClientContainer.instance()
        try:
            container.register_robot_ws(self)
        except Exception as e:
            exception(self, e)

    def on_close(self):
        """@Override"""
        ClientContainer.instance().delete_robot(self.index)

    def on_message(self, response):
        """@Override"""
        ClientContainer.instance().send_to_user(self.index, response)


class UserRegisterHandler(tornado.web.RequestHandler):

    def get(self, index, passphrase):
        container = ClientContainer.instance()
        try:
            container.register_passphrase(index, passphrase)
            self.write(json.dumps({
                'succeeded': True
            }))
        except Exception as e:
            exception(self, e)

    def post(self):
        index = self.get_argument('index')
        passphrase = self.get_argument('passphrase')
        self.get(index, passphrase)


class UserDeleteHandler(tornado.web.RequestHandler):

    def get(self, index):
        container = ClientContainer.instance()
        container.delete_user(index)


class UserSocketHandler(tornado.websocket.WebSocketHandler):

    def check_origin(self, origin):
        """@Override"""
        return True

    def open(self, index, passphrase):
        """@Override"""
        self.index = index
        container = ClientContainer.instance()
        try:
            container.register_user_ws(self)
        except Exception as e:
            exception(self, e)

    def on_close(self):
        """@Override"""
        ClientContainer.instance().delete_user_ws(self.index)

    def on_message(self, response):
        """@Override"""
        ClientContainer.instance().send_to_robot(self.index, response)


class ClientsHandler(tornado.web.RequestHandler):

    def get(self):
        container = ClientContainer.instance()
        self.write(json.dumps(container.get_clients()))


def start_server(port=5000, num_robots_max=1):
    app = tornado.web.Application([
        (r"/robo/register", RobotRegisterHandler),
        (r"/robo/delete", RobotDeleteHandler),
        (r"/robo/([0-9]+)", RobotSocketHandler),
        (r"/user/register", UserRegisterHandler),
        (r"/user/delete", UserDeleteHandler),
        (r"/user/([0-9]+)/([0-9a-zA-Z]+)", UserSocketHandler),
        (r"/clients", ClientsHandler)
    ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()
