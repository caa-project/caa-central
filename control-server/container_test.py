# -*- coding: utf-8 -*-

import unittest
from container import ClientContainer

class WS:

    def __init__(self, index):
        self.index = index

class ClientContainerTest(unittest.TestCase):

    def setUp(self):
        self.container = ClientContainer()

    def test_instance(self):
        container = ClientContainer().instance()
        self.assertNotEqual(container, None)

    def test_add(self):
        self.assertEqual(len(self.container.get_clients()), 0)
        self.assertEqual(self.container.add(), str(0))
        self.assertEqual(len(self.container.get_clients()), 1)

    def test_set_num_max(self):
        self.assertTrue(self.container.set_num_max(3))
        self.assertEqual(self.container.add(), str(0))
        self.assertEqual(self.container.add(), str(1))
        self.assertEqual(self.container.add(), str(2))
        with self.assertRaises(Exception):
            self.container.add()
        self.assertFalse(self.container.set_num_max(2))

    def test_register(self):
        index = self.container.add()
        self.container.register_robot_ws(WS(index))
        with self.assertRaises(Exception):
            self.container.register_robot_ws(WS(index))
        self.container.register_passphrase(index, 'passphrase')
        with self.assertRaises(Exception):
            self.container.register_passphrase(index, 'passphrase')
        self.container.register_user_ws(WS(index))
        with self.assertRaises(Exception):
            self.container.register_user_ws(WS(index))

    def test_delete(self):
        index = self.container.add()
        self.container.register_robot_ws(WS(index))
        self.container.register_passphrase(index, 'passphrase')
        self.container.register_user_ws(WS(index))

        self.container.delete_user_ws(index)
        self.container.register_user_ws(WS(index))

        self.container.delete_user(index)
        self.container.register_user_ws(WS(index))
        self.container.register_passphrase(index, 'passphrase')

        self.container.delete_robot(index)
        with self.assertRaises(Exception):
            self.container.register_robot_ws(WS(index))

if __name__ == '__main__':
    unittest.main()
