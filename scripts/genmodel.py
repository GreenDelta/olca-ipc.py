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
from typing import Optional

from scripts import model

YAML_DIR = path.abspath(path.dirname(__file__)) + '/../../olca-schema/yaml'

def to_snake_case(identifier: str) -> str:
    s = ''
    for char in identifier:
        if char.isupper():
            s += '_'
            s += char.lower()
        else:
            s += char
    # if s is a Python key-word, append a `_`
    if s in ['from', 'in']:
        s += '_'
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
    if model_type == 'date':
        return 'str'
    if model_type == 'GeoJSON':
        return 'dict'
    if model_type.startswith('Ref['):
        return 'Ref'
    if model_type.startswith('List['):
        list_type = py_type(list_elem_type(model_type))
        return f'List[{list_type}]'
    return model_type


def print_class(c: model.ClassType, m: model.Model):
    """Prints a class type."""

    # class declaration
    parent = c.super_class if c.super_class is not None else 'object'
    t = '\n@dataclass\n'
    t += f'class {c.name}({py_type(parent)}):\n'

    # comment
    t += '    """\n'
    t += format_doc(c.doc, 4)
    t += class_attribute_docs(c)
    t += '    """\n\n'

    # attributes
    if c.name == 'Entity':
        t += '    id: str = \'\'\n'
        t += '    olca_type: str = \'\'\n'

    type_label = get_type_label(c)
    if type_label is not None:
        t += f'    olca_type: str = \'{type_label}\'\n'

    for prop in c.properties:
        attr = to_snake_case(prop.name)
        ptype = py_type(prop.field_type)
        t += f'    {attr}: Optional[{ptype}] = None\n'
    print(t)

    # generate _repr_html_ for nice display in Jupyter notebooks
    if c.name == 'Entity':
        r = '''    def _repr_html_(self):
        code = jsonlib.dumps(self.to_json(), indent=2, sort_keys=True)
        if len(code) > 10000:
            code = code[0:10000] + '...'
        return f'<pre><code class="language-json">{code}</code></pre>'
        '''
        print(r)

    print_to_json(c, m)
    print_read_json(c, m)
    print_from_json(c)


def get_type_label(c: model.ClassType) -> Optional[str]:
    """
    Get the type label for the given model class.

    For the data exchange, we need to tag our JSON objects with type labels
    (the '@type' field). In this function we try to find the correct type
    label for the class.
    """
    super_types = ('Entity', 'RootEntity', 'CategorizedEntity')
    if c.name in super_types:
        # no type label for abstract types
        return None
    if c.super_class in super_types:
        return c.name


def print_to_json(c: model.ClassType, m: model.Model):
    t = '    def to_json(self) -> dict:\n'
    off = '        '
    if c.name == 'Entity':
        t += off + "o_type = self.olca_type\n"
        t += off + "if o_type is None:\n"
        t += off + "    o_type = type(self).__name__\n"
        t += off + "json = {'@type': o_type}\n"
        t += off + 'if self.id is not None:\n'
        t += off + "    json['@id'] = self.id\n"
        t += off + 'return json\n'
    else:
        t += off + f'json: dict = super({c.name}, self).to_json()\n'
        for prop in c.properties:
            attr = to_snake_case(prop.name)
            t += off + f'if self.{attr} is not None:\n'
            is_primitive = prop.field_type[0].islower() or \
                           prop.field_type == 'GeoJSON'
            is_enum = m.find_enum(prop.field_type) is not None
            is_list = prop.field_type.startswith('List[')
            if is_primitive:
                t += off + f"    json['{prop.name}'] = self.{attr}\n"
            elif is_enum:
                t += off + \
                     f"    json['{prop.name}'] = self.{attr}.value\n"
            elif is_list:
                t += off + f"    json['{prop.name}'] = []\n"
                t += off + f"    for e in self.{attr}:\n"
                list_type = py_type(list_elem_type(prop.field_type))
                if list_type[0].islower():
                    t += off + off + f"json['{prop.name}'].append(e)\n"
                else:
                    t += off + off + \
                         f"json['{prop.name}'].append(e.to_json())\n"
            else:
                t += off + \
                     f"    json['{prop.name}'] = self.{attr}.to_json()\n"
        t += off + 'return json\n'
    print(t)


def print_from_json(c: model.ClassType):
    t =   '    @staticmethod\n'
    t +=  '    def from_json(json: dict):\n'
    t += f'        instance = {c.name}()\n'
    t +=  '        instance.read_json(json)\n'
    t +=  '        return instance\n'
    print(t)


def print_read_json(c: model.ClassType, m: model.Model):
    t = '    def read_json(self, json: dict):\n'
    off = '        '
    if len(c.properties) == 0:
        t += off + "self.id = json.get('@id')\n"
        t += off + "self.olca_type = json.get('@type')\n"
    else:
        t += off + f'super({c.name}, self).read_json(json)\n'
        for prop in c.properties:
            attr = to_snake_case(prop.name)
            is_primitive = prop.field_type[0].islower() or \
                           prop.field_type == 'GeoJSON'
            is_enum = m.find_enum(prop.field_type) is not None
            is_list = prop.field_type.startswith('List[')
            t += off + f"val = json.get('{prop.name}')\n"
            t += off + "if val is not None:\n"
            if is_primitive:
                t += off + f"    self.{attr} = val\n"
            elif is_enum:
                t += off + \
                     f"    self.{attr} = {prop.field_type}(val)\n"
            elif is_list:
                t += off + f"    self.{attr} = []\n"
                t += off + "    for d in val:\n"
                list_type = list_elem_type(prop.field_type)
                if list_type[0].islower():
                    t += off + off + 'e = d\n'
                else:
                    t += off + off + f'e = {list_type}()\n'
                    t += off + off + 'e.read_json(d)\n'
                t += off + off + f'self.{attr}.append(e)\n'
            else:
                t += off + f"    self.{attr} = {py_type(prop.field_type)}()\n"
                t += off + f"    self.{attr}.read_json(val)\n"
    print(t)


def list_elem_type(list_type: str) -> str:
    """Returns the element type of a list type."""
    t = list_type[5:(len(list_type) - 1)]
    if t.startswith('Ref['):
        return 'Ref'
    return t


def print_enum(e: model.EnumType):
    """Prints an enumeration type."""

    t = f'class {e.name}(Enum):\n'

    # documentation of the enum
    if e.doc is not None:
        t += '    """\n'
        t += format_doc(e.doc, 4)
        t += '\n    """\n\n'

    # enum items
    for item in e.items:
        t += f"    {item.name} = '{item.name}'\n"
        if item.doc is not None:
            t += '    """\n'
            t += format_doc(item.doc, 4)
            t += '\n    """\n\n'
    t += '\n'
    print(t)


def class_attribute_docs(c: model.ClassType) -> str:
    if len(c.properties) == 0:
        return '\n'
    off = '    '
    s = '\n\n'
    s += off + 'Attributes\n'
    s += off + '----------\n'
    for prop in c.properties:
        attr = to_snake_case(prop.name)
        ptype = py_type(prop.field_type)
        s += f'{off}{attr}: {ptype}\n'
        doc = format_doc(prop.doc, indent=8)
        if doc == '':
            s += '\n'
        else:
            s += doc + '\n\n'
    return s


def format_doc(doc: str, indent: int = 4) -> str:
    if doc is None:
        return ''
    text = doc.strip()
    if text == '':
        return text

    # split the text into words
    words = []
    word = ''
    for char in text:
        if char.isspace():
            if len(word) > 0:
                words.append(word)
                word = ''
            continue
        word += char
    if len(word) > 0:
        words.append(word)

    text = ''
    line = ' ' * indent
    for word in words:
        if len(line) > indent:
            _line = line + ' ' + word
        else:
            _line = line + word
        if len(_line) > 79:
            text += line + '\n'
            line = ' ' * indent + word
        else:
            line = _line
    text += line

    return text


if __name__ == '__main__':
    print('# DO NOT CHANGE THIS CODE AS THIS IS GENERATED AUTOMATICALLY\n')
    print('# This module contains a Python API of the JSON-LD based')
    print('# openLCA data exchange model.package schema.')
    print('# For more information see '
          'http://greendelta.github.io/olca-schema/\n')
    print('from __future__ import annotations\n')
    print('import json as jsonlib\n')
    print('from dataclasses import dataclass')
    print('from enum import Enum')
    print('from typing import List, Optional\n\n')

    m = model.Model.load_yaml(YAML_DIR)  # type: model.Model
    for enum in m.enums:
        print_enum(enum)
    for clazz in m.classes:
        print_class(clazz, m)
