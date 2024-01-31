import json

class ConfigurationService:
    def __init__(self, configFileName) -> None:
        config = json.load(open(configFileName))
        self.pcIp:str = config["pcIp"]
        self.gpioPin:int = config["gpioPin"]
        self.remainOn:int = config["remainOn"]
        self.timeout:int = config["timeout"]
        self.port:int = config["port"]
        self.host:str = config["host"]