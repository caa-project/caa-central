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
        self.container.add('1024')
        self.assertEqual(len(self.container.get_clients()), 1)

    def test_set_num_max(self):
        self.assertTrue(self.container.set_num_max(3))
        self.container.add('1024')
        self.container.add('2')
        self.container.add('512')
        with self.assertRaises(Exception):
            self.container.add()
        self.assertFalse(self.container.set_num_max(2))

    def test_register(self):
        index = '1024'
        self.container.add(index)
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
        index = '1024'
        self.container.add(index)
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

    def test_clients(self):
        index = '1024'
        self.container.add(index)
        self.container.register_robot_ws(WS(index))
        self.container.register_passphrase(index, 'passphrase')
        self.container.register_user_ws(WS(index))
        client_dict = self.container.get_clients()
        self.assertIn(index, client_dict)
        self.assertIn('robot_ws', client_dict[index])
        self.assertIn('user_ws', client_dict[index])
        self.assertNotIn('passphrase', client_dict[index])
        self.assertIn('using', client_dict[index])
        client_dict = self.container.get_clients()
        self.assertIn(index, client_dict)
        self.assertIn('robot_ws', client_dict[index])
        self.assertIn('user_ws', client_dict[index])
        self.assertNotIn('passphrase', client_dict[index])
        self.assertIn('using', client_dict[index])

if __name__ == '__main__':
    unittest.main()
