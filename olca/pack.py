import json
import logging as log
import zipfile

import olca.schema as schema


class Writer(object):

    def __init__(self, file_name: str):
        self.__zip = zipfile.ZipFile(
            file_name, mode='a', compression=zipfile.ZIP_DEFLATED)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def close(self):
        self.__zip.close()

    def write(self, entity: schema.Entity):
        if not isinstance(entity, schema.Entity):
            log.error('%s is not an instance of Entity; skipped it', entity)
            return
        path = _get_path(entity)
        if path is None:
            path = 'unknown'
        obj = entity.to_json()
        self.write_json(obj, path)

    def write_json(self, obj: dict, folder: str):
        uid = obj.get('@id')
        if uid is None or uid == '':
            log.error('No @id for object %s in %s', obj, folder)
            return
        path = '%s/%s.json' % (folder, uid)
        s = json.dumps(obj)
        self.__zip.writestr(path, s)


def _get_path(entity: schema.Entity):
    if entity is None:
        return None
    t = type(entity)
    if t == schema.Category:
        return "categories"
    # if t == schema.Currency:
    #    return "currencies"
    if t == schema.Process:
        return "processes"
    if t == schema.Flow:
        return "flows"
    if t == schema.FlowProperty:
        return "flow_properties"
    if t == schema.Actor:
        return "actors"
    if t == schema.ImpactCategory:
        return "lcia_categories"
    if t == schema.ImpactMethod:
        return "lcia_methods"
    if t == schema.Location:
        return "locations"
    # if t == schema.NwSet:
    #    return "nw_sets"
    if t == schema.Parameter:
        return "parameters"
    if t == schema.ProductSystem:
        return "product_systems"
    # if t == schema.Project:
    #    return "projects"
    if t == schema.SocialIndicator:
        return "social_indicators"
    if t == schema.Source:
        return "sources"
    if t == schema.Unit:
        return "units"
    if t == schema.UnitGroup:
        return "unit_groups"
    # if t == schema.DqSystem:
    #    return "dq_systems"
    log.warning('Unknown entity type %s', t)
    return None
