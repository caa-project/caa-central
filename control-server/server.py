#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Control Server

@TODO
- UI Server以外の接続に対しエラー
- pass_dictを直接触るの嫌なのでクラスをつくる
"""


import tornado.httpserver
import tornado.web
import tornado.websocket


# indexとpassphraseの組み合わせ
pass_dict = dict()


class Constants():
    NUM_ROBOTS_MAX = 0


class KillHandler(tornado.web.RequestHandler):

    def get(self, index):
        # TODO mutex lock
        if index in pass_dict:
            del pass_dict[index]
            self.write("Killed index '%s'" % index)
        else:
            self.set_status(500, "no such index '%s'" % index)


class CreateHandler(tornado.web.RequestHandler):

    def get(self, index, passphrase):
        if index in pass_dict:
            # TODO エラーを吐く
            self.set_status(500, "Already exists")
        elif len(pass_dict) >= Constants.NUM_ROBOTS_MAX:
            # TODO エラーを吐く
            self.set_status(500, "Too many")
        else:
            pass_dict[index] = passphrase
            self.write("Created index '%s'" % index)


class DumpHandler(tornado.web.RequestHandler):

    def get(self):
        response = ""
        for index, passphrase in pass_dict.iteritems():
            response += "%s: %s<br>" % (index, passphrase)
        self.write(response)


class RobotHandler(tornado.websocket.WebSocketHandler):

    robot_ws_dict = dict()

    def check_origin(self, origin):
        return True

    def open(self, index):
        # 同じindexに対して１つしか繋がない
        if index in RobotHandler.robot_ws_dict:
            print "Already exits"
            self.close(403, "Already exits")
        else:
            print "Connected to %s" % index
            RobotHandler.robot_ws_dict[index] = self

    def on_message(self, response):
        # TODO レスポンスのログをとる
        print response
        self.write_message("hi")

    @classmethod
    def write_message_to(cls, index, operation):
        """ロボットに命令を送る

        UIから命令を含んだリクエストをもらったら呼ばれるよ．
        """
        cls.robot_ws_dict[index].write_message(operation)


class OperationHandler(tornado.web.RequestHandler):

    def get(self, index, passphrase):
        # check index and passphrase
        # get json
        operation = "operation"
        RobotHandler.write_message_to(index, operation)


def start_server(port=5000, num_robots_max=1):
    Constants.NUM_ROBOTS_MAX = num_robots_max
    app = tornado.web.Application([
        (r"/create/([0-9]+)/([0-9a-zA-Z]+)", CreateHandler),
        (r"/dump", DumpHandler),
        (r"/kill/([0-9]+)", KillHandler),
        (r"/operation/([0-9]+)/([0-9a-zA-Z]+)", OperationHandler),
        (r"/robo/([0-9]+)", RobotHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()
