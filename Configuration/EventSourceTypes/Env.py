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
