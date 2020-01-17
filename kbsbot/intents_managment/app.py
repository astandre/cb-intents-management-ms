import os
from flakon import create_app as _create_app
from .views import blueprints
import configparser

_HERE = os.path.dirname(__file__)
_SETTINGS = os.path.join(_HERE, 'settings.ini')


def create_app(settings=None):
    if settings is None:
        settings = _SETTINGS
    config = configparser.ConfigParser()
    config.read(_SETTINGS)

    print(config.read(_SETTINGS))
    for key in config["flask"]:
        print(config["flask"][key])
        os.environ[key] = config["flask"][key]

    app = _create_app(blueprints=blueprints, settings=settings)
    return app
