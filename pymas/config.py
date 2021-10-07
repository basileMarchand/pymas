import pathlib as pl 
import yaml 

from pymas.utils import logger


class ConfigNotFound(Exception):
    pass

class FieldInConfigNotFound(Exception):
    pass

class FieldInconfigNotValid(Exception):
    pass


def need_config( func ):
    def internal(klass, *args):
        if not klass._config.exists():
            raise ConfigNotFound("No configuration file found")
        klass._config.load()
        if not klass.hasConfig():
            raise ConfigNotFound("No valide smtp configuration found")
        return func(klass, *args)
    return internal


def need_save( func ):
    def internal(klass, *args):
        func(klass, *args)
        klass.save()
    return internal 

def need_valid(func):
    def internal(klass, *args):
        klass.isValid()
        return func(klass, *args)
    return internal

class PyMasConfig:
    default = {
        "smtp_server": None,
        "smtp_port": None,
        "smtp_login": None, 
        "from_address": None
    }

    def __init__(self):
        self._path = (pl.Path("~") / ".pymas.yml" ).expanduser() 
        self._data = {}


    def exists(self) -> bool:
        return self._path.exists()


    def load(self):
        with self._path.open("r") as fid:
            self._data = yaml.safe_load(fid)

    def loadIfExists(self):
        if self.exists():
            self.load()

    def save(self):
        with self._path.open("w") as fid:
            yaml.safe_dump(self._data, fid)

    def isValid(self):
        for key in PyMasConfig.default.keys():
            if not key in self._data:
                raise FieldInConfigNotFound(f"field {key} doesn't exists in config file. Specify it using\n    pymas config --{key} <value>")
            elif (self._data[key] is None) or (self._data[key] == "" ):
                raise FieldInconfigNotValid(f"field {key} value is not valid. Specify it using\n    pymas config --{key} <value>")
        return True

    @need_valid
    def get(self, field):
        return self._data[field]

    @need_save
    def set(self, field, value):
        self._data[field] = value 


if __name__ == "__main__":
    c = PyMasConfig()
    c.loadIfExists()
    try:
        c.get("smtp_server")
    except FieldInConfigNotFound as e: 
        print(e)


    c.set("smtp_server", "fake.smtp.fr")
    #c.set("smtp_port", 587)