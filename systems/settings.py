
def readSetting(fcontent, settingName):
    for line in fcontent:
        if line.startswith(settingName):
            return line.split(":")[1][:-1]
    return None


def formatSetting(settingName, settingValue):
    return f"{settingName}:{settingValue}\n"


def saveSettings(fHandle, content):
    for line in content:
        fHandle.write(line)


class Settings:
    def __init__(self):
        self.settings = {
            "width": 800,
            "height": 600,
            "fullscreen": False,
            "fps": 60,
            "title": "Worms ékip 10",
        }
        self.settings_types = {
            "width": int,
            "height": int,
            "fullscreen": bool,
            "fps": int,
            "title": str,
        }
        try:
            settings_file = open("settings.txt", "r")
            fcontent = settings_file.readlines()
            settings_file.close()
            for setting in self.settings:
                self.settings[setting] = readSetting(fcontent, setting)
        except FileNotFoundError:
            settings_file = open("settings.txt", "w")
            for setting in self.settings:
                settings_file.write(formatSetting(setting, self.settings[setting]))
            settings_file.close()

        for setting in self.settings:
            if self.settings_types[setting] != bool:
                setattr(self, setting, self.settings_types[setting](self.settings[setting]))
            else:
                setattr(self, setting, self.settings[setting] == "True")
