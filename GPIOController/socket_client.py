#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""socket_client

サーバーとWebSocketを使って通信を行い，送られてきた命令に従ってGPIOの制御をする．

"""

from GPIOControler.safety import SafetyThread
from GPIOControler.wheel import WheelControler
# from GPIOControler.servo import ServoBlaster
import json
import fixedphrase
import websocket
from jtalk import say

# サーボの準備> 0 = p1pin12 = GPIO18
# GPIOControler.servo.initialize([12], 150)

# 車輪の制御
wh = WheelControler([11, 13, 15, 16])
# サーボの制御
# sv = ServoBlaster(0, 0.075)
# 安全装置
th = SafetyThread(10)


def handle_data(data):
    """dataに従って命令を送るオブジェクトを変える

    いまはサーボとモータしかないので，適当
    - サーボの命令
        - servoXX XX=-60~60
    - モータの命令
        - forward
        - back
        (以下略)
    """
    # if data["type"] == "servo":
    #     print "@servo", data["value"]
    #     sv.move(data["value"])
    #     return True
    if data["type"] == "wheel":
        print "@wheel", data["value"]
        wh.execute(data["value"])
        return True
    if data["type"] == "say":
        msg = data["value"].encode("utf-8")
        print "@say", msg
        say(msg)
        return True
    if data["type"] == "fixedphrase":
        fixedphrase.say(int(data["value"]))
        return True
    return False


def on_message(ws, msg):
    """受信時のコールバック関数

    受け取った命令に従って動作をする．動作が成功したかどうかを返事する．
    """
    data = json.loads(msg)
    try:
        result = handle_data(data)
        data['success'] = result
        if result:
            th.update()
        else:
            data["reason"] = "oh no!"
    except Exception as e:
        data["success"] = False
        data["reason"] = str(e)
    ws.send(json.dumps(data))


def on_error(ws, error):
    """エラー時のコールバック
    """
    print error


def on_close(ws):
    """接続が閉じた時のコールバック
    """
    print "### closed ###"


def on_open(ws):
    """接続開始時のコールバック
    """
    print "### open ###"


def init_safety():
    # 安全装置の稼働
    th.register(wh.stop)
    th.start()


def get_websocket(server):
    ws = websocket.WebSocketApp(server,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    return ws
