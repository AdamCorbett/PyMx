import urllib.request
from pprint import pprint


class MobotixConfigSection:
    """
    Defines a section from a Mobotix camera configuration file
    Each section is a key=value pair
    This version currently does not handle the JSON sections.
    """
    def __init__(self, name, items):
        self.name = name.strip()
        self.items = {}
        if '.json' in name:
            self.items = items
        else:
            for item in items:
                k, v = item.split('=', 1)
                self.items[k] = v


class MobotixConfig:
    """
    Holds the items that make up a Mobotix Camera configuration file
    Lines beginning with a # are comments and are not included in this
    Note: That means that comments may be lost when we write back
    the configuration file.
    """
    def __init__(self, data):
        self.sections = []
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
                    self.sections.append(MobotixConfigSection(section_name, items))
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
        data += "view configfile\n"
        data += "quit\n"

        data = bytes(data.encode("ascii"))
        handler = self.opener.open(self.config_path.format(self.ip), data=data)
        return handler.read()

    def get_image(self, size="3072x2048"):
        return self.opener.open(self.image_path.format(self.ip, size)).read()

    def update(self):
        self.image_data = self.get_image()


if __name__ == '__main__':
    # M = MobotixCam("127.0.0.1:8001")
    M = MobotixCam("184.183.156.98:39")
    # M = MobotixCam()
    cfg = MobotixConfig(M.get_config().decode('utf-8'))
    # print(cfg.decode('utf-8'))
    for section in cfg.sections:
        pprint(section.name)
        pprint(section.items)
        pprint("-------------------------")
