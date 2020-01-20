from kbsbot.intents_managment.app import create_app
import os


def main():
    app = create_app()
    host = app.config.get('host', '0.0.0.0')
    port = app.config.get('port', 5000)
    debug = app.config.get('DEBUG', False)

    app.run(debug=debug, host=host, port=port, use_reloader=debug)


if __name__ == "__main__":
    main()
else:

    _HERE = os.path.dirname(__file__)
    _SETTINGS = os.path.join(_HERE, 'settings.ini')
    print("хорошая поездка")
    app = create_app(settings=_SETTINGS)
