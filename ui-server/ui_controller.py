# -*- coding: utf-8 -*-

import string
import random
import logging
import control_proxy

logging.basicConfig(format='%(asctime)-15s | %(message)s')


class PassGenerator():
    """Generate passphrase"""

    def __init__(self, charset=string.ascii_letters+"0123456789"):
        self.charset = charset

    def generate(self, length=64):
        passphrase = ""
        for i in range(length):
            passphrase += random.choice(self.charset)
        return passphrase


class UIController():

    def __init__(self, control_server_url):
        self._pass_dict = {}
        self.control_server_url = control_server_url
        self.proxy = control_proxy.ControlProxy(control_server_url)
        self.pass_generator = PassGenerator()
        self.logger = logging.getLogger('caa.ui_controller')
        self.logger.setLevel(logging.DEBUG)
        self.reset_message()

    def register(self, index):
        passphrase = self.pass_generator.generate()
        try:
            response = self.proxy.register(index, passphrase)
            if 'success' in response and response['success']:
                self._pass_dict[index] = passphrase
                self.success("Registered %s : %s" % (index, passphrase))
                return True
            else:
                self.danger(response['message'])
        except Exception as e:
            self.error(e)
        except:
            self.danger("Unknown error")
        return False

    def delete(self, index):
        if index not in self._pass_dict:
            self.danger('Do not have an access to %s' % index)
            return False
        try:
            passphrase = self._pass_dict[index]
            response = self.proxy.delete(index, passphrase)
            if response['success']:
                self._pass_dict.pop(index)
                self.success("Deleted %s" % index)
                return True
            else:
                self.danger(response['message'])
        except Exception as e:
            self.error(e)
        except:
            self.danger("Unknown error")
        return False

    def robo_register(self, index):
        try:
            response = self.proxy.robo_register(index)
            if 'success' in response and response['success']:
                return True
            else:
                self.danger(response['message'])
        except Exception as e:
            self.error(e)
        except:
            self.danger("Unknown error")
        return False
                
    def robo_delete(self, index):
        try:
            response = self.proxy.robo_delete(index)
            if 'success' in response and response['success']:
                return True
            else:
                self.danger(response['message'])
        except Exception as e:
            self.error(e)
        except:
            self.danger("Unknown error")
        return False

    def get_clients(self):
        try:
            return self.proxy.get_clients()
        except Exception as e:
            self.error(e)
        return {}

    def indexes(self):
        return self._pass_dict

    def clear(self):
        for index in self._pass_dict:
            self.proxy.delete(index, self._pass_dict[index])
        self._pass_dict.clear()

    def auth(self, index, passphrase):
        return (index in self._pass_dict
                and self._pass_dict[index] == passphrase)

    def reset_message(self):
        self.phase = 'info'
        self.message = ''

    def get_message(self):
        retval = (self.phase, self.message)
        self.reset_message()
        return retval

    def success(self, message):
        self.phase = 'info'
        self.message = message
        self.logger.info(message)

    def warn(self, message):
        self.phase = 'warn'
        self.message = message
        self.logger.warning(message)

    def danger(self, message):
        self.phase = 'danger'
        self.message = message
        self.logger.error(message)

    def error(self, e):
        self.phase = 'danger'
        self.message = 'Error: %s' % e
        self.logger.exception(e)

    def passphrase(self, index):
        if index in self._pass_dict:
            return self._pass_dict[index]
        return None
