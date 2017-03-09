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
        self.activity_area = [0, 95, 22, 1078, 805]
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
            self.activity_area = [int(x) for x in param_dict.get('activity_area', []).split(',')]
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


class MobotixCam:
    def __init__(self, ip="192.168.10.40",
                 username="admin", password="meinsm"):
        self.ip = ip
        self.url = "http://{0}/".format(ip)

        password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, self.url, username, password)
        handler = urllib.request.HTTPBasicAuthHandler(password_mgr)

        self.opener = urllib.request.build_opener(handler)

        self.image_path = "http://{0}/cgi-bin/image.jpg?size={1}&quality=90"
        self.config_path = "http://{0}/admin/remoteconfig"
        self.image_data = None
        # self.get_image()

    def get_config(self):
        data = "\n"
        data += "helo\n"
        data += "view section events\n"
        data += "quit\n"

        data = bytes(data.encode("ascii"))
        handler = self.opener.open(self.config_path.format(self.ip), data=data)
        return handler.read()

    def get_image(self, size="3072x2048"):
        return self.opener.open(self.image_path.format(self.ip, size)).read()

    def update(self):
        self.image_data = self.get_image()


if __name__ == '__main__':
    M = MobotixCam()
    cfg = MobotixConfig(M.get_config().decode('utf-8'))
    # print(cfg.decode('utf-8'))

    pprint(cfg.sections['events'].items['AS'].__dict__)
