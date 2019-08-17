from Camera import Camera
from Configuration.Configuration import Configuration
from Configuration.EmailSettings import EmailSettings
from Configuration.EventSources import EventSources

if __name__ == '__main__':
    Cam = Camera("192.168.0.158", "admin", "Phx2Jdl1!")
    Conf = Configuration(Cam)
    Mail = EmailSettings(Conf)
    Events = EventSources(Conf)
    print(Events)
