# -*- coding: utf-8 -*-

from container import ClientContainer

import tornado.httpserver
import tornado.web
import tornado.websocket
import json
import logging

logger = logging.getLogger("caa.control.api")

def exception(handler, error):
    logger.exception(error)
    handler.write(json.dumps({
        'success': False,
        'reason': str(error)
    }))

def exception_on_socket(handler, no, error):
    logger.exception(error)
    handler.close(no, str(error))

class RobotRegisterHandler(tornado.web.RequestHandler):

    def get(self):
        index = self.get_argument('index')
        container = ClientContainer.instance()
        try:
            container.add(index)
            self.write(json.dumps({
                'success': True,
                'index': index
            }))
        except Exception as e:
            exception(self, e)
        self.finish()


class RobotDeleteHandler(tornado.web.RequestHandler):

    def get(self):
        index = self.get_argument('index')
        container = ClientContainer.instance()
        if container.delete_robot(index):
            self.write(json.dumps({'success': True}))
        else:
            self.write(json.dumps({'success': False}))
        self.finish()


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
            exception_on_socket(self, 403, e)

    def on_close(self):
        """@Override"""
        ClientContainer.instance().delete_robot_ws(self.index)

    def on_message(self, response):
        """@Override"""
        ClientContainer.instance().send_to_user(self.index, response)


class UserRegisterHandler(tornado.web.RequestHandler):

    def get(self):
        self.register()

    def post(self):
        self.register()

    def register(self):
        index = self.get_argument('index')
        passphrase = self.get_argument('passphrase')
        container = ClientContainer.instance()
        try:
            container.register_passphrase(index, passphrase)
            self.write(json.dumps({
                'success': True
            }))
        except Exception as e:
            exception(self, e)
        self.finish()


class UserDeleteHandler(tornado.web.RequestHandler):

    def get(self):
        index = self.get_argument('index')
        container = ClientContainer.instance()
        if container.delete_user(index):
            self.write(json.dumps({'success': True}))
        else:
            self.write(json.dumps({'success': False}))
        self.finish()


class UserSocketHandler(tornado.websocket.WebSocketHandler):

    def check_origin(self, origin):
        """@Override"""
        return True

    def open(self, index, passphrase):
        """@Override"""
        container = ClientContainer.instance()
        if not container.auth(index, passphrase):
            self.write("")
            return
        self.index = index
        try:
            container.register_user_ws(self)
        except Exception as e:
            exception_on_socket(self, 403, e)

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
        self.finish()


def start_server(port=5000, num_robots_max=1):
    ClientContainer.instance().set_num_max(num_robots_max)
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
