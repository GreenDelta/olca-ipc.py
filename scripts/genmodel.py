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

YAML_DIR = '../../olca-schema/yaml'


import yaml
from os import listdir


def to_snake_case(identifier: str) -> str:
    s = ''
    for char in identifier:
        if char.isupper():
            s += '_'
            s += char.lower()
        else:
            s += char
    return s


def print_class(model):
    name = model['name']
    parent = model['superClass'] if 'superClass' in model else 'object'
    t = 'class %s(%s):\n\n' % (name, parent)
    t += '    def __init__(self):\n'
    if 'properties' in model:
        for prop in model['properties']:
            attr = to_snake_case(prop['name'])
            t += '        self.%s = None  # type: %s\n' % (attr, prop['type'])
    print(t)


def convert_property(prop):
    name = prop['name']    
    t = name[0].upper() + name[1:]
    type = prop['type']
    if type == 'integer':
        t += ' int' + (' `json:"%s"`' % name)
    elif type == 'double':
        t += ' float64' + (' `json:"%s"`' % name)
    elif type == 'boolean':
        t += ' bool' + (' `json:"%s"`' % name)
    elif type == 'date' or type == 'dateTime':
        t += ' string' + (' `json:"%s,omitempty"`' % name)
    elif type == 'List[string]':
        t += ' []string' + (' `json:"%s,omitempty"`' % name)
    elif type.startswith('List['):
        sub = type[5:(len(type)-1)]
        t += ' []' + sub + (' `json:"%s,omitempty"`' % name)    
    else:
        t += ' ' + type + (' `json:"%s,omitempty"`' % name)
    return t


def print_constructor(class_model):
    if 'superClass' not in class_model:
        return
    name = class_model['name']
    s = class_model['superClass']
    if s != 'RootEntity' and s != 'CategorizedEntity':
        return
    t = '// New%s initializes a new %s with the given id and name\n' % (name, name)
    v = name[0].lower()
    t += 'func New%s(id, name string) *%s {\n' % (name, name)
    t += '\t%s := %s{}\n' % (v, name)
    t += '\t%s.Context = ContextURL\n' % v
    t += '\t%s.Type = "%s"\n' % (v, name)
    t += '\t%s.ID = id\n' % v
    t += '\t%s.Name = name\n' % v
    t += '\treturn &%s\n' % v
    t += '}\n'    
    print(t)    


if __name__ == '__main__':
    print('# This module contains a Python API of the JSON-LD based')
    print('# openLCA data exchange model.package schema.')
    print('# For more information see http://greendelta.github.io/olca-schema/\n')
    for f in listdir(YAML_DIR):
        path = YAML_DIR + '/' + f
        with open(path, 'r', encoding='utf-8') as stream:
            model = yaml.load(stream)
            if 'class' in model:
                print_class(model['class'])