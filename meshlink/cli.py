
import argparse


def main():
    parser = argparse.ArgumentParser(
        prog="meshlink",
        description="Peer-to-peer chat and file sharing",
    )

    parser.add_argument(
        "--version",
        action="version",
        version="meshlink 0.0.1",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    subparsers.add_parser("host", help="Start a host")

    connect_parser = subparsers.add_parser(
        "connect",
        help="Connect to a peer",
    )
    connect_parser.add_argument("ip", help="Peer IP address")

    args = parser.parse_args()

    if args.command == "host":
        from threaded_host import run_host
        run_host()

    elif args.command == "connect":
        from threaded_client import run_client
        run_client(args.ip)


if __name__ == "__main__":
    main()
