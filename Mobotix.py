import urllib.request
from pprint import pprint


class MobotixConfigEventProfile:
    def __init__(self):
        self.type = ''
        self.profilename = ''
        self.profilestate = ''
        self.ima_dead = '5'
        self.ima_sense = 'as'
        self.activity_level = ''
        self.activity_area = [0, 0, 0, 1280, 960]
        self.activity_directions = 'Left;Right;Up;Down'
        self.ot_type = 'corridor'
        self.vmlist = ''
        self.default_width = 1280
        self.default_height = 960

    def set_from_config(self, line):
        params = line.split(':')
        param_type = params.pop(0)
        self.type, v = param_type.split('=')
        if self.type == 'ima':
            param_dict = dict(s.split('=') for s in params)
            self.profilename = param_dict['_profilename']
            self.ima_dead = param_dict.get('ima_dead', '')
            self.ima_sense = param_dict.get('ima_sense', '')
            self.activity_level = param_dict.get('activity_level', '')
            self.activity_area = [int(x) for x in param_dict.get('activity_area', '').split(',')]
            self.activity_directions = param_dict.get('activity_directions', '')


class MobotixConfigSection:
    def __init__(self, name, items):
        self.name = name.strip()
        self.items = {}
        if '.json' in name:
            self.items = items
        else:
            for item in items:
                if self.name == 'events':
                    mxevent = MobotixConfigEventProfile()
                    mxevent.set_from_config(item)
                    self.items[mxevent.profilename] = mxevent
                else:
                    k, v = item.split('=', 1)
                    self.items[k] = v


class MobotixConfig:
    def __init__(self, data):
        self.sections = {}
        self.parse_config(data)

    def parse_config(self, data):
        section_name = ""
        items = []
        for line in data.splitlines(True):
            if len(line.strip()) > 0 and not line.startswith("#") and not line.startswith("OK"):
                words = line.split()
                if words[0] == "SECTION":
                    section_name = words[1]
                elif words[0] == "ENDSECTION":
                    self.sections[section_name] = MobotixConfigSection(section_name, items)
                    items = []
                else:
                    items.append(line)
