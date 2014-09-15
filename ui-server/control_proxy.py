#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
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

    def _fetch_json(self, *path):
        """Fetch Json response from Control Server.
        If response is error, raise Exception with error reason
        """
        try:
            url = self._get_url(*path)
            response = urllib2.urlopen(url)
            return json.loads(response.read())
        except urllib2.URLError as e:
            if hasattr(e, "reason"):
                msg = e.reason
            elif hasattr(e, "code"):
                msg = "Error code %d" % e.code
            raise Exception(msg)
        except:
            raise Exception("Unknown error")

    def delete(self, index):
        return self._fetch_json("delete", index)

    def register(self, index, passphrase):
        return self._fetch_json("register", index, passphrase)
