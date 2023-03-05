# file format:
# settingName:settingValue:[possibleValues]

# example:
# width:800:[800,1020,1280,1600,1920]
def read_setting(fcontent, setting_name):
    for line in fcontent:
        if line.startswith(setting_name):
            return line.split(":")[1]
    return None


def format_setting(setting_name, setting_value, setting_possible_values):
    return f"{setting_name}:{setting_value}:{setting_possible_values}]\n"


def read_possible_values(fcontent, setting_name):
    for line in fcontent:
        if line.startswith(setting_name):
            return line.split(":")[2][1:-2].split(",")
    return None


def save_settings(fhandle, content):
    for line in content:
        fhandle.write(line)


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
                self.settings[setting] = read_setting(fcontent, setting)
                self.possibleValues[setting] = read_possible_values(fcontent, setting)
                if self.settings_types[setting] == int:
                    self.possibleValues[setting] = [int(x) for x in self.possibleValues[setting]]
                elif self.settings_types[setting] == bool:
                    self.possibleValues[setting] = [x == "True" for x in self.possibleValues[setting]]
        except FileNotFoundError:
            settings_file = open("settings.txt", "w")
            for setting in self.settings:
                settings_file.write(format_setting(setting, self.settings[setting], self.possibleValues[setting]))
            settings_file.close()

        for setting in self.settings:
            if self.settings_types[setting] != bool:
                setattr(self, setting, self.settings_types[setting](self.settings[setting]))
            else:
                setattr(self, setting, self.settings[setting] == "True")
