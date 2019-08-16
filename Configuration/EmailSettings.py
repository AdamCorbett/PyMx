from Configuration.Configuration import Configuration


class EmailSettings:

    config_section = "mail"

    """
    Tool for working with Mobotix Camera Email settings
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

        self.from_address = ""
        self.reply_address = ""
        self.mail_body = ""
        self.security = ""
        self.auth = ""
        self.smtp = ""
        self.pop3 = ""
        self.mail_user = ""
        self.mail_pass = ""

        self.profiles = []

        self.parseconfig()

    def parseconfig(self):
        pass
        for item in self.config_data:
            # Split Item into Key: Value
            # If Key is "Profile" create a new Profile
            # Otherwise set the appropriate class property
            k, v = item.split('=', 1)
            if k == "profile":
                self.profiles.append(EmailProfile.from_config(item))
            else:
                if k == "from":
                    self.from_address = v
                if k == "reply":
                    self.reply_address = v
                if k == "body":
                    self.mail_body = v
                if k == "auth":
                    self.auth = v
                if k == "smtp":
                    self.smtp = v
                if k == "pop3":
                    self.pop3 = v
                if k == "user":
                    self.mail_user = v
                if k == "pass":
                    self.mail_pass = v

    def __repr__(self):
        output = "Configuration data for {0}\n".format(self.section_name)
        output += "from: {0}\n".format(self.from_address)
        output += "reply: {0}\n".format(self.reply_address)
        output += "body: {0}\n".format(self.mail_body)
        output += "security: {0}\n".format(self.security)
        output += "auth: {0}\n".format(self.auth)
        output += "smtp: {0}\n".format(self.smtp)
        output += "pop3: {0}\n".format(self.pop3)
        output += "user: {0}\n".format(self.mail_user)
        output += "pass: {0}\n".format(self.mail_pass)
        output += "Email Profiles: {0}\n".format(len(self.profiles))
        for profile in self.profiles:
            output += "\t{}\n".format(profile)
        return output


class EmailProfile:
    def __init__(self):
        self.profile = ""  # mail0..mail99
        self._profilename = ""
        self.rcpt = ""
        self.subj = ""
        self.attach = ""  # img|clip|sysmsg
        self.imgprof = ""  # section: imagelink:profile
        self.filetype = ""  # mxg|jpg
        self.rate100 = 100
        self.antetime = 1
        self.posttime = 1
        self.systime = 0
        self.smime = 0

        self.from_address = ""
        self.reply_address = ""
        self.mail_body = ""
        self.security = ""
        self.auth = ""
        self.smtp = ""
        self.pop3 = ""
        self.mail_user = ""
        self.mail_pass = ""

    def __repr__(self):
        return "Email Profile: {0} {1}".format(self.profile, self._profilename)

    @staticmethod
    def from_config(config_line):
        profile = EmailProfile()
        items = config_line.split(':')
        for item in items:
            k, v = item.split('=', 1)
            if k == "profile":
                profile.profile = v  # mail0..mail99
            if k == "_profilename":
                profile._profilename = v
            if k == "rcpt":
                profile.rcpt = v
            if k == "subj":
                profile.subj = v
            if k == "attach":
                profile.attach = v  # img|clip|sysmsg
            if k == "imgprof":
                profile.imgprof = v  # section: imagelink:profile
            if k == "filetype":
                profile.filetype = v  # mxg|jpg
            if k == "rate100":
                profile.rate100 = v
            if k == "antetime":
                profile.antetime = v
            if k == "posttime":
                profile.posttime = v
            if k == "systime":
                profile.systime = v
            if k == "smime":
                profile.smime = v

            if k == "from":
                profile.from_address = v
            if k == "reply":
                profile.reply_address = v
            if k == "body":
                profile.mail_body = v
            if k == "auth":
                profile.auth = v
            if k == "smtp":
                profile.smtp = v
            if k == "pop3":
                profile.pop3 = v
            if k == "user":
                profile.mail_user = v
            if k == "pass":
                profile.mail_pass = v

        return profile
