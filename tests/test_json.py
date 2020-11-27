import unittest

import olca


class TestJson(unittest.TestCase):

    def test_ref(self):
        ref = olca.ref(olca.Flow, 'co2', 'CO2')
        json = ref.to_json()
        self.assertEqual('Flow', json['@type'])
        self.assertEqual('co2', json['@id'])
        self.assertEqual('CO2', json['name'])

    def test_type_tags(self):
        instances = [
            olca.Actor(),
            olca.Source(),
            olca.Unit(),
            olca.UnitGroup(),
            olca.FlowProperty(),
            olca.SocialIndicator(),
            olca.Flow(),
            olca.Process(),
            olca.ImpactCategory(),
            olca.ImpactMethod(),
            olca.ProductSystem(),
            olca.Project(),
        ]
        for i in instances:
            json = i.to_json()
            self.assertEqual(type(i).__name__, json['@type'])


if __name__ == '__main__':
    unittest.main()
