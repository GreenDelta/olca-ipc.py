import requests

import olca.schema as schema

from typing import List, Type


class Client(object):

    def __init__(self, port):
        self.url = 'http://localhost:%i' % port
        self.next_id = 1

    def insert(self, model: Type[schema.RootEntity]):
        if model is None:
            return
        json = model.to_json()
        return self.__post('insert/model', json)

    def update(self, model: Type[schema.RootEntity]):
        if model is None:
            return
        json = model.to_json()
        return self.__post('update/model', json)

    def calculate(self, setup: schema.CalculationSetup) -> schema.SimpleResult:
        if setup is None:
            return
        return self.__post('calculate', setup.to_json())

    def get_descriptors(self, model_type) -> List[schema.Ref]:
        """
        Get the list of descriptors of the entities with the given
        model type.
        :param model_type: A class, e.g. olca.Flow
        :return: A list of descriptors.
        """
        params = {'@type': model_type.__name__}
        result = self.__post('get/descriptors', params)
        descriptors = []
        for r in result:
            d = schema.Ref()
            d.from_json(r)
            descriptors.append(d)
        return descriptors

    def get(self, model_type, id: str):
        params = {'@type': model_type.__name__, '@id': id}
        result = self.__post('get/model', params)
        e = model_type()
        e.from_json(result)
        return e

    def get_process(self, id: str) -> schema.Process:
        return self.get(schema.Process, id)

    def __post(self, method: str, params):
        req = {
            'jsonrpc': '2.0',
            'id': self.next_id,
            'method': method,
            'params': params
        }
        self.next_id += 1
        resp = requests.post(self.url, json=req).json()  # type: dict
        err = resp.get('error')  # type: dict
        if err is not None:
            raise Exception('%i: %s' % (err.get('code'), err.get('message')))
        result = resp.get('result')
        if result is None:
            raise Exception(
                'No error and no result: invalid JSON-RPC response')
        return result
