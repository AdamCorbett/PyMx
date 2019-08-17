from Configuration.Configuration import Configuration
from Configuration.EventSourceTypes.Env import Env
from Configuration.EventSourceTypes.Ima import Ima
from Configuration.EventSourceTypes.Sig import Sig
from Configuration.EventSourceTypes.Tim import Tim


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

        self._load_from_config()

    def _load_from_config(self):
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
