#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Control Server

@TODO
- UI Server以外の接続に対しエラー
"""


import tornado.httpserver
import tornado.web
import tornado.websocket


class Auth():
    """Singleton class for authorization.
    This class sotres pair of index and passphrase in a dictionary.
    To get instance, call static method instance().

    Example:
        auth = Auth.instance()
        auth.register("1", "abc123")
        auth.auth("1", "abc123")    # True
        auth.auth("1", "a")         # False
    """
    def __init__(self):
        self._pass_dict = dict()
        self._num_max = 1

    def register(self, index, passphrase):
        if len(self._pass_dict) >= self._num_max:
            raise Exception("Too many indexes")
        if index in self._pass_dict:
            raise Exception("Index already exists")
        self._pass_dict[index] = passphrase

    def delete(self, index):
        if index in self._pass_dict:
            del self._pass_dict[index]
        else:
            raise Exception("No such index")

    def auth(self, index, passphrase):
        if index not in self._pass_dict:
            return False
        if self._pass_dict[index] == passphrase:
            return True
        else:
            return False

    def set_num_max(self, num):
        """登録できる最大数の設定"""
        self._num_max = num

    def num_max(self):
        return self._num_max

    def dump(self):
        response = ""
        response += "robo: %d/%d\n" % (RobotHandler.size(), self.num_max())
        response += "client: %d/%d\n" % (len(self._pass_dict), self.num_max())
        for k, v in self._pass_dict.iteritems():
            response += "%s: %s\n" % (k, v)
        return response

    def _clear(self):
        """Use only in tests"""
        self._pass_dict.clear()

    @staticmethod
    def instance():
        if not hasattr(Auth, "_instance"):
            Auth._instance = Auth()
        return Auth._instance

    @staticmethod
    def initialized():
        return hasattr(Auth, "_instance")


class DeleteHandler(tornado.web.RequestHandler):

    def get(self, index):
        # TODO mutex lock
        try:
            Auth.instance().delete(index)
            self.write("Deleted index '%s'" % index)
        except Exception as e:
            print e.message
            self.set_status(500, e.message)


class RegisterHandler(tornado.web.RequestHandler):

    def get(self, index, passphrase):
        try:
            Auth.instance().register(index, passphrase)
            self.write("Registered index '%s'" % index)
        except Exception as e:
            print e.message
            self.set_status(500, e.message)


class DumpHandler(tornado.web.RequestHandler):

    def get(self):
        self.write(Auth.instance().dump().replace("\n", "<br>"))


class RobotHandler(tornado.websocket.WebSocketHandler):

    ws_dict = dict()

    def check_origin(self, origin):
        """@Override"""
        return True

    def open(self, index):
        """@Override"""
        print "open"
        # 同じindexに対して１つしか繋がない
        if index in RobotHandler.ws_dict:
            print "Already exits"
            self.close(403, "Already exits")
        elif len(RobotHandler.ws_dict) >= Auth.instance().num_max():
            print "Too many"
            self.close(403, "Too many")
        else:
            print "Connected to %s" % index
            RobotHandler.ws_dict[index] = self
            self.index = index

    def on_close(self):
        """@Override"""
        print "Closed %s" % self.index
        RobotHandler.ws_dict.pop(self.index)

    def on_message(self, response):
        """@Override"""
        # TODO レスポンスのログをとる
        print response

    @classmethod
    def write_message_to(cls, index, operation):
        """ロボットに命令を送る

        UIから命令を含んだリクエストをもらったら呼ばれるよ．
        """
        if index in cls.ws_dict:
            cls.ws_dict[index].write_message(operation)

    @classmethod
    def size(cls):
        return len(RobotHandler.ws_dict)


class OperationHandler(tornado.websocket.WebSocketHandler):

    ws_dict = dict()

    def check_origin(self, origin):
        """@Override"""
        return True

    def open(self, index, passphrase):
        """@Override"""
        if not Auth.instance().auth(index, passphrase):
            print "Auth failed"
            self.close(403, "Auth failed")
        elif index in OperationHandler.ws_dict:
            print "Already exits"
            self.close(403, "Already exits")
        else:
            print "Connected to %s" % index
            OperationHandler.ws_dict[index] = self
            self.index = index

    def on_close(self):
        """@Override"""
        print "Closed %s" % self.index
        OperationHandler.ws_dict.pop(self.index)

    def on_message(self, operation):
        """@Override"""
        RobotHandler.write_message_to(self.index, operation)


def start_server(port=5000, num_robots_max=1):
    Auth.instance().set_num_max(num_robots_max)
    app = tornado.web.Application([
        (r"/delete/([0-9]+)", DeleteHandler),
        (r"/dump", DumpHandler),
        (r"/operation/([0-9]+)/([0-9a-zA-Z]+)", OperationHandler),
        (r"/register/([0-9]+)/([0-9a-zA-Z]+)", RegisterHandler),
        (r"/robo/([0-9]+)", RobotHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()
