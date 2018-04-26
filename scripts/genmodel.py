"""
This is a script for generating the initial model types from the
olca-schema yaml files. To run this script you need to have PyYAML
installed, e.g.:

    pip install pyyaml

You also have to configure the YAML_DIR in this script to point to
the directory where the YAML files are located: 
    # clone the olca-schema repository to some folder
    cd <folder>
    git clone https://github.com/GreenDelta/olca-schema.git
    # <folder>/olca-schema/yaml is the path for the YAML_DIR

After this you can run this script. It will print the generated classes and
enumerations to the console:

    python genmodel.py > [.. path to generated file].py

"""

from os import path

import model


YAML_DIR = path.abspath(path.dirname(__file__)) + '/../../olca-schema/yaml'


def to_snake_case(identifier: str) -> str:
    s = ''
    for char in identifier:
        if char.isupper():
            s += '_'
            s += char.lower()
        else:
            s += char
    return s


def py_type(model_type: str) -> str:
    if model_type == 'string':
        return 'str'
    if model_type == 'double':
        return 'float'
    if model_type == 'boolean':
        return 'bool'
    if model_type == 'integer':
        return 'int'
    if model_type == 'dateTime':
        return 'str'
    return model_type


def print_class(c: model.ClassType, m: model.Model):
    parent = c.super_class if c.super_class is not None else 'object'
    t = 'class %s(%s):\n\n' % (c.name, parent)
    t += '    def __init__(self):\n'
    if len(c.properties) == 0:
        t += '        pass\n'
    else:
        t += '        super(%s, self).__init__()\n' % (c.name)
    for prop in c.properties:
        attr = to_snake_case(prop.name)
        ptype = py_type(prop.field_type)
        t += '        self.%s = None  # type: %s\n' % (attr, ptype)
    print(t)
    print_to_json(c, m)


def print_to_json(c: model.ClassType, m: model.Model):
    t = '    def to_json(self) -> dict:\n'
    off = '        '
    if len(c.properties) == 0:
        t += off + 'return {}\n'
    else:
        t += off + 'jdict = super(%s, self).to_json()  # type: dict\n' % c.name
        for prop in c.properties:
            attr = to_snake_case(prop.name)
            t += off + 'if self.%s is not None:\n' % attr
            is_primitive = prop.field_type[0].islower()
            is_enum = m.find_enum(prop.field_type) is not None
            is_list = prop.field_type.startswith('List[')
            if is_primitive:
                t += off + "    jdict['%s'] = self.%s\n" % (prop.name, attr)
            elif is_enum:
                t += off + \
                    "    jdict['%s'] = self.%s.value\n" % (prop.name, attr)
            elif is_list:
                t += off + "    jdict['%s'] = []\n" % (prop.name)
                t += off + "    for e in %s:\n" % (attr)
                t += off + off + \
                    "jdict['%s'].append(e.to_json())\n" % (prop.name)
            else:
                t += off + \
                    "    jdict['%s'] = self.%s.to_json()\n" % (prop.name, attr)
        t += off + 'return jdict\n'
    print(t)


def print_enum(e: model.EnumType):
    t = 'class %s(Enum):\n' % e.name
    for item in e.items:
        t += "    %s = '%s'\n" % (item.name, item.name)
    t += '\n'
    print(t)


if __name__ == '__main__':
    print('# This module contains a Python API of the JSON-LD based')
    print('# openLCA data exchange model.package schema.')
    print('# For more information see '
          'http://greendelta.github.io/olca-schema/\n')
    print('from enum import Enum\n')

    m = model.Model.load_yaml(YAML_DIR)  # type: model.Model
    for e in m.enums:
        print_enum(e)
    for c in m.classes:
        print_class(c, m)
