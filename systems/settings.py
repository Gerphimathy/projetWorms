# file format:
# settingName:settingValue:[possibleValues]

# example:
# width:800:[800,1020,1280,1600,1920]
def readSetting(fcontent, settingName):
    for line in fcontent:
        if line.startswith(settingName):
            return line.split(":")[1]
    return None


def formatSetting(settingName, settingValue, settingPossibleValues):
    return f"{settingName}:{settingValue}:{settingPossibleValues}]\n"

def readPossibleValues(fcontent, settingName):
    for line in fcontent:
        if line.startswith(settingName):
            return line.split(":")[2][1:-2].split(",")
    return None

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
        self.possibleValues = {
            "width": [800, 1020, 1280, 1600, 1920, 2560],
            "height": [600, 720, 800, 900, 1080, 1440],
            "fullscreen": [True, False],
            "fps": [30, 60, 120],
            "title": ["Worms ékip 10", "Worms ékip 10 - Fullscreen"],
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
                self.possibleValues[setting] = readPossibleValues(fcontent, setting)
                if self.settings_types[setting] == int:
                    self.possibleValues[setting] = [int(x) for x in self.possibleValues[setting]]
                elif self.settings_types[setting] == bool:
                    self.possibleValues[setting] = [x == "True" for x in self.possibleValues[setting]]
        except FileNotFoundError:
            settings_file = open("settings.txt", "w")
            for setting in self.settings:
                settings_file.write(formatSetting(setting, self.settings[setting], self.possibleValues[setting]))
            settings_file.close()

        for setting in self.settings:
            if self.settings_types[setting] != bool:
                setattr(self, setting, self.settings_types[setting](self.settings[setting]))
            else:
                setattr(self, setting, self.settings[setting] == "True")
