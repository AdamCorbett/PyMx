from Configuration.Configuration import Configuration
from Configuration.EventSourceTypes.ImaActivityArea import ActivityArea


class Ima:
    def __init__(self, item):
        self.type = "ima"
        self.profile = ""
        self._profilename = ""
        self._profilestate = ""
        self.ima_sense = ""  # vm|as
        self.vm_list = ""
        self.activity_level = ""
        self.activity_area = []
        self.activity_direction = ""
        self.ot_type = ""

        self.parse(item)

    def parse(self, item):
        for config in item.split(':'):
            # Split configuration entry into key/value pair
            k, v = config.split('=', 1)
            if k == "ima":  # key matches EventSourceType, value matches Event Profile Name
                self.profile = v
            elif k == "activity_area":  # Special handling needed for Activity Area, may include multiple values
                areas = Configuration.string_decode(v).splitlines(False)
                for area in areas:
                    new_area = ActivityArea(area)
                    self.activity_area.append(new_area)
            elif k == "activity_directions":
                self.activity_direction = v
            else:
                if hasattr(self, k):
                    setattr(self, k, v)

    def __repr__(self):
        activity = ""
        for area in self.activity_area:
            activity += str(area) + "\n\t\t"

        return "{0} {1} {2}\n\t\t{3}".format(self.type, self.profile, self._profilename, activity)
