# -*- coding: utf-8 -*-

import unittest
from container import ClientContainer

class ClientContainerTest(unittest.TestCase):

    def setUp(self):
        self.container = ClientContainer()

    def test_instance(self):
        container = ClientContainer().instance()
        self.assertNotEqual(container, None)

if __name__ == '__main__':
    unittest.main()
