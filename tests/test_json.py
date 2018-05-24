import unittest

import olca


class TestJson(unittest.TestCase):

    def test_ref(self):
        ref = olca.ref(olca.Flow, 'co2', 'CO2')
        json = ref.to_json()
        self.assertEqual('Flow', json['@type'])
        self.assertEqual('co2', json['@id'])
        self.assertEqual('CO2', json['name'])


if __name__ == '__main__':
    unittest.main()
