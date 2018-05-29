import requests

import olca.schema as schema

from typing import List, Type, TypeVar


T = TypeVar('T')


class Client(object):
    """
    An instance of Client holds a connection and provides a set of methods in
    order to communicate with an openLCA IPC server.
    """

    def __init__(self, port):
        self.url = 'http://localhost:%i' % port
        self.next_id = 1

    def insert(self, model: schema.RootEntity):
        if model is None:
            return
        json = model.to_json()
        return self.__post('insert/model', json)

    def update(self, model: schema.RootEntity):
        if model is None:
            return
        json = model.to_json()
        return self.__post('update/model', json)

    def calculate(self, setup: schema.CalculationSetup) -> schema.SimpleResult:
        if setup is None:
            raise ValueError('Invalid calculation setup')
        resp = self.__post('calculate', setup.to_json())
        result = schema.SimpleResult()
        result.from_json(resp)
        return result

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

    def get(self, model_type: Type[T], model_id: str) -> T:
        params = {'@type': model_type.__name__, '@id': model_id}
        result = self.__post('get/model', params)
        e = model_type()
        e.from_json(result)
        return e

    def find(self, model_type, name: str) -> schema.Ref:
        """Searches for a data set with the given type and name.

        :param model_type: The class of the data set, e.g. `olca.Flow`.
        :param name: The name of the data set.
        :return: The reference to the first data set with the given name and
                 type from the databases or ``None`` if there is no such data
                 set in the database.
        """
        for d in self.get_descriptors(model_type):
            if d.name == name:
                return d

    def dispose(self, entity: schema.Entity):
        """
        Removes the given entity from the memory of the IPC server.  This is
        required for calculation results that are hold on the server for
        further processing.

        :param entity: The entity that should be disposed.
        """
        if entity is None:
            return
        arg = {'@type': type(entity).__name__, '@id': entity.id}
        self.__post('dispose', arg)

    def __post(self, method: str, params) -> dict:
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
