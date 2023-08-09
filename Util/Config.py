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
        if Config.data is None: 
            try:
                Config.data = toml.load(Config.path)
            except FileNotFoundError as error:
                print("Config file could not be loaded. Maybe it does not exist.")
                raise error
            except toml.TomlDecodeError as error:
                print("Config file contained invalid TOML syntax and could not be loaded.")
                raise error
        return Config.data
    
    def debug() -> bool:
        """Use this method to check whether debug mode is on. (Shorthand of Config.get)

        Returns:
            bool: Debug state
        """
        data: dict = Config.get()
        return data["development"]["debug"]
            