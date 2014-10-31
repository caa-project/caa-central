# -*- coding: utf-8 -*-

import threading

class ClientContainerItem():

    def __init__(self):
        self.robot_ws = None
        self.clear_user()

    def clear_user(self):
        self.user_ws = None
        self.passphrase = None

    def __iter__(self):
        return self.__dict__.iteritems()

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value


def synchronized(fun):
    def wrap(self, *args, **kwargs):
        with self.lock:
            return fun(self, *args, **kwargs)
    return wrap


class ClientContainer():

    _instance = None

    def __init__(self):
        self._clients = dict()
        self.lock = threading.Lock()
        self.set_num_max(1)

    @synchronized
    def set_num_max(self, num):
        if num < len(self._clients):
            return False
        self._num_max = num
        return True

    @synchronized
    def get_num_max(self):
        return self._num_max

    @synchronized
    def add(self, index):
        if len(self._clients) >= self._num_max:
            raise Exception('Can not register more clients')
        if index in self._clients:
            raise Exception('%s is already used.' % index)
        self._clients[index] = ClientContainerItem()

    @synchronized
    def register_robot_ws(self, ws):
        if ws.index not in self._clients:
            raise Exception('The index %s is not registered.' % ws.index)
        if self._clients[ws.index].robot_ws is not None:
            raise Exception('Already registered at the index %s.' % ws.index)
        self._clients[ws.index].robot_ws = ws

    @synchronized
    def delete_robot_ws(self, index):
        if index in self._clients:
            self._clients[index].robot_ws = None
            return True
        return False

    @synchronized
    def delete_robot(self, index):
        if index in self._clients:
            #self._clients[index].robot_ws = None
            self._clients.pop(index)
            return True
        return False

    @synchronized
    def register_passphrase(self, index, passphrase):
        if index not in self._clients:
            raise Exception('The index %s is not registered.' % index)
        if self._clients[index].passphrase is not None:
            raise Exception('Already registered at the index %s.' % index)
        self._clients[index].passphrase = passphrase

    @synchronized
    def register_user_ws(self, ws):
        if ws.index not in self._clients:
            raise Exception('The index %s is not registered.' % ws.index)
        if self._clients[ws.index].user_ws is not None:
            raise Exception('Already registered at the index %s.' % ws.index)
        self._clients[ws.index].user_ws = ws

    @synchronized
    def delete_user_ws(self, index):
        if index in self._clients:
            self._clients[index].user_ws = None
            return True
        return False

    @synchronized
    def delete_user(self, index):
        if index in self._clients:
            self._clients[index].clear_user()
            return True
        return False

    @synchronized
    def auth(self, index, passphrase):
        if index in self._clients and self._clients[index].passphrase == passphrase:
            return True
        return False

    @synchronized
    def send_to_robot(self, index, message):
        if index in self._clients and self._clients[index].robot_ws is not None:
            self._clients[index].robot_ws.write_message(message)

    @synchronized
    def send_to_user(self, index, message):
        if index in self._clients and self._clients[index].user_ws is not None:
            self._clients[index].user_ws.write_message(message)

    @synchronized
    def get_clients(self):
        retval = {}
        for index in self._clients:
            retval[index] = {}
            for key, value in self._clients[index]:
                retval[index][key] = value
            retval[index]['using'] = retval[index]['passphrase'] is not None
            retval[index]['robot_ws'] = retval[index]['robot_ws'] is not None
            retval[index]['user_ws'] = retval[index]['user_ws'] is not None

            del retval[index]['passphrase']
        return retval

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

