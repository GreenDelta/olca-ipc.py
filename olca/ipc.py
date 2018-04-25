import requests

import olca.schema as schema


class Client(object):

    def __init__(self, port):
        self.url = 'http://localhost:%i' % port

    def insert(model: schema.RootEntity):
        if model is None:
            return
        pass
