from Configuration.Configuration import Configuration
from Configuration.EventSourceTypes.ImaActivityArea import ActivityArea


class Ima:
    def __init__(self):
        self.type = "ima"
        self.profile = ""
        self._profilename = ""
        self._profilestate = ""
        self.ima_dead = ""  # vm|as
        self.ima_sens = ""  # vm|as
        self.vm_list = ""
        self.activity_level = ""
        self.activity_areas = []
        self.activity_directions = ""
        self.ot_type = ""

    @staticmethod
    def create_from_config(config):
        """

        :param config:  Config line from "events" section of Mobotix camera configfile
        :return: Ima (Image) type Event Source object
        """
        event_source = Ima()

        for setting in config.split(':'):
            # Split configuration entry into key/value pair
            k, v = setting.split('=', 1)
            if k == "ima":  # key matches EventSourceType, value matches Event Profile Name
                event_source.profile = v
            elif k == "activity_area":  # Special handling needed for Activity Area, may include multiple values
                areas = Configuration.string_decode(v).splitlines(False)
                for area in areas:
                    new_area = ActivityArea(area)
                    event_source.activity_areas.append(new_area)
            elif k == "activity_directions":
                event_source.activity_direction = v
            else:
                if hasattr(event_source, k):
                    setattr(event_source, k, v)
        return event_source

    @staticmethod
    def to_config_line(event):
        """

        :type event: Ima
        :param event:
        :return:
        """
        activity_text = ""
        area: ActivityArea
        for area in event.activity_areas:
            activity_text += area.to_config_line()

        output = (f"{event.type}={event.profile}:_profilename={event._profilename}:_profilestate={event._profilestate}:"
                  f"ima_dead={event.ima_dead}:ima_sens={event.ima_sens}:activity_level:{event.activity_level}:"
                  f"vm_list={event.vm_list}:ot_type={event.ot_type}:activity_directions={event.activity_directions}:"
                  f"activity_area={activity_text}")

        return output

    def __repr__(self):
        activity = ""
        for area in self.activity_areas:
            activity += str(area) + "\n\t\t"

        return "{0} {1} {2}\n\t\t{3}".format(self.type, self.profile, self._profilename, activity)
