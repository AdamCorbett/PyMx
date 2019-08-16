from Camera import Camera
import urllib.parse


class Configuration:

    remote_config_wrapper = "\nhelo\n{0}\nquit\n"
    remote_config_path_wrapper = "http://{0}/admin/remoteconfig"

    """
    Tools to load and update Mobotix Camera Configuration
    """
    def __init__(self, camera: Camera):
        """
        :param camera: a Mobotix Camera object
        """
        self.camera = camera
        self.remote_config_path = Configuration.remote_config_path_wrapper.format(self.camera.ip)

    def get_all_config(self):
        """
        Load entire Config File from camera
        :return: Configuration Data
        """
        data = Configuration.remote_config_wrapper.format("view configfile")
        return self._get_config(data)

    def get_config_section(self, section="events"):
        """
        Load a specific section from the camera's configuration
        :param section: Section Name
        :return: Configuration Data
        """
        section = "view section {0}".format(section)
        data = Configuration.remote_config_wrapper.format(section)
        return self._get_config(data)

    def _get_config(self, data):
        """
        Internal Method
        Performs actual configuration request for camera.
        :param data: Configuration Request String
        :return: Configuration Data
        """
        data = bytes(data.encode("ascii"))
        handler = self.camera.opener.open(self.remote_config_path, data=data)
        return handler.read().decode('utf-8')

    @staticmethod
    def parse_config_data(raw_data):
        """
        Convert the raw Configuration data into a list: 1 entry per line
        :param raw_data:
        :return:  section_name, items_list
        """
        section_name = "NOT_SET"
        items = []
        for line in raw_data.splitlines(True):
            if len(line.strip()) > 0 and not line.startswith("#") and not line.startswith("OK"):
                words = line.split()
                if words[0] == "SECTION":
                    section_name = words[1]
                elif words[0] == "ENDSECTION":
                    pass
                else:
                    items.append(line.strip())
        return section_name, items

    @staticmethod
    def config_string(text):
        return urllib.parse.quote(text)

