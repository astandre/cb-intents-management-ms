from kbsbot.intents_managment.app import create_app
import signal
import sys
import argparse


def _quit(signal, frame):
    print("Bye!")
    # add any cleanup code here
    sys.exit(0)


def main(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description='Intents Managment')

    parser.add_argument("-d", "--deploy", default=False, help="Pass to generate app wsgi object", dest="deploy",
                        action='store_true')
    parser.add_argument('--config-file', help='Config file',
                        type=str, default=None)
    args = parser.parse_args(args=args)
    print(args.config_file)
    app = create_app(args.config_file)
    host = app.config.get('host', '0.0.0.0')
    port = app.config.get('port', 5000)
    debug = app.config.get('DEBUG', False)

    signal.signal(signal.SIGINT, _quit)
    signal.signal(signal.SIGTERM, _quit)

    if args.deploy is False:
        app.run(debug=debug, host=host, port=port, use_reloader=debug)
        # return app
    else:
        print("хорошая поездка")
        return app


# def main():
#     app = create_app()
#     host = app.config.get('host', '0.0.0.0')
#     port = app.config.get('port', 5000)
#     debug = app.config.get('DEBUG', False)
#
#     signal.signal(signal.SIGINT, _quit)
#     signal.signal(signal.SIGTERM, _quit)
#
#     app.run(debug=debug, host=host, port=port, use_reloader=debug)


if __name__ == "__main__":
    main()
# else:
#     _HERE = os.path.dirname(__file__)
#     _SETTINGS = os.path.join(_HERE, 'settings.ini')
#     print(_SETTINGS)
#     print("хорошая поездка")
#     app = create_app(settings=_SETTINGS)
