# This file contains the Config class.
# This class is used for enabling the bot to read the options selected by the user in the config.toml file
# The config.toml file allows any user, regardless of programming ability, to easily modify parameters
# that the bot uses for runs.

import toml

class Config:
    """
    Class to handle reading the config.toml file
    """
    data = None
    path: str = "config.toml"
    
    def getParam(paramName: str) -> any:
        """Shorthand for returing the content of a specific parameter from the config file.

        Args:
            paramName (str): Name of the parameter in the config.toml file under parameters.

        Raises:
            KeyError: The accessed parameter does not exist in the config file.

        Returns:
            any: Content of the desired parameter.
        """
        params: dict = Config.get()["parameters"]
        if paramName in params: return params[paramName]
        else: 
            print(f"Accessed config parameter {paramName} does not exist.")
            raise KeyError()
    
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
            