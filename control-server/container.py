# -*- coding: utf-8 -*-

class ClientContainerItem():

    def __init__(self):
        self.robot_ws = None
        self.clear_user()

    def clear_user(self):
        self.user_ws = None
        self.passphrase = None

class ClientContainer():

    _instance = None

    def __init__(self):
        self._clients = dict()
        self.set_num_max(1)

    def set_num_max(self, num):
        if num < len(self._clients):
            return False
        self._num_max = num
        return True

    def get_num_max(self):
        return self._num_max

    def add(self):
        if len(self._clients) >= self._num_max:
            raise Exception('Can not register more clients')
        for i in range(self._num_max):
            index = str(i)
            if index not in self._clients:
                self._clients[index] = ClientContainerItem()
                return index
        raise Exception('Something wrong has occered!')

    def register_robot_ws(self, ws):
        if ws.index not in self._clients:
            raise Exception('The index %s is not registered.' % ws.index)
        if self._clients[ws.index].robot_ws is not None:
            raise Exception('Already registered at the index %s.' % ws.index)
        self._clients[ws.index].robot_ws = ws

    def delete_robot(self, index):
        if index in self._clients:
            #self._clients[index].robot_ws = None
            self._clients.pop(index)

    def register_passphrase(self, index, passphrase):
        if index not in self._clients:
            raise Exception('The index %s is not registered.' % index)
        if self._clients[index].passphrase is not None:
            raise Exception('Already registered at the index %s.' % index)
        self._clients[index].passphrase = passphrase

    def register_user_ws(self, ws):
        if ws.index not in self._clients:
            raise Exception('The index %s is not registered.' % ws.index)
        if self._clients[ws.index].user_ws is not None:
            raise Exception('Already registered at the index %s.' % ws.index)
        self._clients[ws.index].user_ws = ws

    def delete_user_ws(self, index):
        if index in self._clients:
            self._clients[index].user_ws = None

    def delete_user(self, index):
        if index in self._clients:
            self._clients[index].clear_user()

    def auth(self, index, passphrase):
        if index in self._clients and self._clients[index].passphrase == passphrase:
            return True
        return False

    def send_to_robot(self, index, message):
        if index in self._clients and self._clients[index].robot_ws is not None:
            self._clients[index].robot_ws.write_message(message)

    def send_to_user(self, index, message):
        if index in self._clients and self._clients[index].user_ws is not None:
            self._clients[index].user_ws.write_message(message)

    def get_clients(self):
        return self._clients

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

