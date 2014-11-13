#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import urllib
import urllib2
import urlparse


class ControlProxy():
    """Control APIとのやりとりをするクラス

    AdminHandlerからこいつを使ってControl Serverとやりとりをする．
    """

    def __init__(self, control_server_url):
        """
        @param control_server_url: Control Server's url
            e.g. localhost:5000
        """
        self.control_server_url = control_server_url

    def _get_url(self, *path):
        """Example:
            _get_url("foo", "bar") # (control_server_url)/foo/bar
        """
        url = urlparse.urljoin(self.control_server_url, "")
        for elem in path:
            url = urlparse.urljoin(url+"/", elem)
        return url

    def _fetch_json(self, *path, **args):
        """Fetch Json response from Control Server.
        If response is error, raise Exception with error reason
        """
        url = self._get_url(*path)
        if len(args) != 0:
            url = '%s?%s' % (url, urllib.urlencode(args))
        response = urllib2.urlopen(url)
        return json.loads(response.read())

    def delete(self, index, passphrase):
        return self._fetch_json("user", "delete", index=index, passphrase=passphrase)

    def register(self, index, passphrase):
        return self._fetch_json("user", "register", index=index, passphrase=passphrase)

    def get_clients(self):
        return self._fetch_json("clients")
