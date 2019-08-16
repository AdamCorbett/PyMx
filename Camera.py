import urllib.request


class Camera:
    image_path = "cgi-bin/image.jpg?size={1}&quality=90"

    def __init__(self, ip="192.168.0.10",
                 username="admin", password="meinsm"):
        """
        Create new Camera Connection
        :param ip: Camera IP Address
        :param username: Login Name
        :param password: Login Password (Cleartext)
        """
        self.ip = ip
        self.url = "http://{0}/".format(ip)
        self.image_url = self.url + Camera.image_path
        # self.remote_config_path = Configuration.remote_config_path_wrapper.format(ip)

        password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, self.url, username, password)
        handler = urllib.request.HTTPBasicAuthHandler(password_mgr)

        self.opener = urllib.request.build_opener(handler)

    def perform_request(self, data):
        return self.opener.open(data).read()

    def get_image(self, size="3072x2048"):
        return self.perform_request(self.image_url.format(size))
