from Configuration.Configuration import Configuration


class EventSources:

    config_section = "events"

    """
    Tool for working with Mobotix Camera Event Sources
    """
    def __init__(self, configuration: Configuration):
        """
        :param configuration: a Mobotix Camera object
        """
        self.configuration = configuration
        self.raw_config = configuration.get_config_section(self.config_section)

        self.section_name, self.config_data = Configuration.parse_config_data(self.raw_config)

        if self.section_name != self.config_section:
            raise("Invalid Configuration Section {0}!  Was expecting {1}".format(self.section_name,
                                                                                 self.config_section))

        self.events = []

        self.parseconfig()

    def parseconfig(self):
        for item in self.config_data:
            # Split Item into Key: Value

            k, v = item.split('=', 1)
            if k == "env":
                self.events.append(Env(item))
            if k == "ima":
                self.events.append(Ima(item))
            if k == "sig":
                self.events.append(Sig(item))
            if k == "tim":
                self.events.append(Tim(item))

    def __repr__(self):
        output = "Configuration data for {0}\n".format(self.section_name)
        output += "Event Profiles: {0}\n".format(len(self.events))
        for event in self.events:
            output += "\t{}\n".format(event)
        return output


class Env:
    def __init__(self, item):
        self.item = item
        self.type = "env"
        self.profile = ""
        self._profilename = ""
        self._profilestate = ""
        self.env_dead = 0
        self.env_sense = ""  # ir, mi, il, tp
        # il_src
        # il_lvl
        # ir_src
        # ir_lvl
        # mi_lvl
        # mi_wid
        # tp_src
        # tp_lvl
        # tp_unit
        # pos_anchor
        # pos_dist
        # pos_unit
        # vel_max
        # vel_unit  # m/s
        # uhu_type
        # uhu_act
        # uhu_unit
        # uhu_lvl
        # uhu_lvl_cmp
        # uhu_range_min
        # uhu_range_max
        # uhu_range_cmp
        # ev_env_ima_uhu_area
        # ev_env_ima_uhu_mode
        # ev_env_ima_uhu_millipercent
        # ev_env_ima_uhu_act
        # ev_env_ima_uhu_reference_area
        # ev_env_ima_uhu_cmp
        # ev_env_ima_uhu_show_area
        # ev_env_ima_ugu_show_meter
        # ev_env_ima_uhu_show_name
        # ara_area
        # ara_measurement_mode
        # ara_mode
        # ara_millipercent
        # ara_type
        # ara_act
        # ara_unit
        # ara_lvl
        # ara_reference_area
        # ara_reference_tolerance
        # ara_lvl_cmp
        # ara_range_min
        # ara_range_max
        # ara_range_cmp
        # ara_show_area
        # ara_show_meter
        # ara_show_temperature
        # ara_show_coordinates
        # ara_show_crosshairs
        # ara_show_name
        # env_cmp
        # env_act

    def __repr__(self):
        return "{0} {1} {2}".format(self.type, self.profile, self._profilename)


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
            # Split Item into Key: Value

            k, v = config.split('=', 1)
            if k == "ima":
                self.profile = v
            elif k == "activity_area":
                # self.activity_area = v
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


class ActivityArea:
    def __init__(self, area):
        self.camera = 0
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.poly = []
        self.parse(area)

    def parse(self, area):
        values = area.split(',')
        self.camera = values[0]
        if values[1].startswith("poly"):
            points = values[1].split('=')[1]
            for point in points.split('/'):
                x, y = point.split('x')
                self.poly.append((x, y))
        else:
            self.x = values[1]
            self.y = values[2]
            self.width = values[3]
            self.height = values[4]

    def __repr__(self):
        if len(self.poly) == 0:
            return "{0}: ({1}, {2}), ({3}, {4})".format(self.camera, self.x, self.y, self.width, self.height)
        else:
            points = []
            for point in self.poly:
                points.append("({0}, {1})".format(point[0], point[1]))
            return "{0}: [{1}]".format(self.camera, "-".join(points))


class Sig:
    def __init__(self, item):
        self.item = item
        self.type = "sig"
        self.profile = ""
        self._profilename = ""
        self._profilestate = ""

    def __repr__(self):
        return "{0} {1} {2}".format(self.type, self.profile, self._profilename)


class Tim:
    def __init__(self, item):
        self.item = item
        self.type = "tim"
        self.profile = ""
        self._profilename = ""
        self._profilestate = ""

    def __repr__(self):
        return "{0} {1} {2}".format(self.type, self.profile, self._profilename)
