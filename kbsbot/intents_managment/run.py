from kbsbot.intents_managment.app import create_app
import sys
import signal
from chaussette.server import make_server
from werkzeug.serving import run_with_reloader
import argparse


def _quit(signal, frame):
    print("Bye!")
    # add any cleanup code here
    sys.exit(0)


def main(args=sys.argv[1:]):
# def main():
    parser = argparse.ArgumentParser(description='Intents Managment')

    parser.add_argument('--fd', type=int, default=None)
    parser.add_argument('--config-file', help='Config file',
                        type=str, default=None)
    args = parser.parse_args(args=args)

    app = create_app(args.config_file)
    # app = create_app()
    host = app.config.get('host', '0.0.0.0')
    port = app.config.get('port', 5000)
    debug = app.config.get('DEBUG', False)

    signal.signal(signal.SIGINT, _quit)
    signal.signal(signal.SIGTERM, _quit)

    def runner():
        if args.fd is not None:
            # use chaussette
            httpd = make_server(app, host='fd://%d' % args.fd)
            httpd.serve_forever()
        else:
            app.run(debug=debug, host=host, port=port, use_reloader=debug)

    if not debug:
        runner()
    else:
        run_with_reloader(runner)
    app.run(debug=debug, host=host, port=port, use_reloader=debug)


if __name__ == "__main__":
    main()
