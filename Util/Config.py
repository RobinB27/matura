import toml

class Config:
    """
    Class to handle reading the config.toml file
    """
    data = None
    path: str = "config.toml"
    
    def get() -> dict:
        """Use this method to acces the config file's content

        Returns:
            dict: Dict-conversion of config.toml
        """
        if Config.data is None: Config.data = toml.load(Config.path)
        return Config.data
    
    def debug() -> bool:
        """Use this method to check whether debug mode is on. (Shorthand of Config.get)

        Returns:
            bool: Debug state
        """
        data: dict = Config.get()
        return data["development"]["debug"]
            