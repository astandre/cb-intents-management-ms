from kbsbot.intents_managment.app import create_app
import os


if __name__ == "__main__":
    _HERE = os.path.dirname(__file__)
    _SETTINGS = os.path.join(_HERE, 'settings.ini')
    app = create_app(settings=_SETTINGS)
    host = app.config.get('host', '0.0.0.0')
    port = app.config.get('port', 5000)
    debug = app.config.get('DEBUG', False)
    app.run(debug=debug, host=host, port=port, use_reloader=debug)
else:
    _HERE = os.path.dirname(__file__)
    _SETTINGS = os.path.join(_HERE, 'settings.ini')
    print("хорошая поездка")
    app = create_app(settings=_SETTINGS)
