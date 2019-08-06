import ujson as json


class Config():

    def config_load(self, configFile):
        # global sensor, hubAddress, deviceId, sharedAccessKey, owmApiKey, owmLocation
        try:
            print('Loading {0} settings'.format(configFile))

            config_data = open(configFile)
            config = json.load(config_data)

            self.ssid = config['ssid']
            self.password = config['password']
            self.host = config['host']
            self.key = config['key']
            self.deviceId = config['deviceId']
            self.sampleRate = config['sampleRate']
            
        except:
            print('Error loading config data')

    def __init__(self, configFile):
        self.config_load(configFile)