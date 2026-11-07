"""Start the platform API: python -m aigcm.api [--host 0.0.0.0] [--port 8770]."""

import argparse

import uvicorn

from . import create_app


def main(argv=None):
    parser = argparse.ArgumentParser(prog="aigcm.api", description=__doc__)
    parser.add_argument("--host", default="127.0.0.1",
                        help="127.0.0.1 (default) for this laptop only; 0.0.0.0 for the home network")
    parser.add_argument("--port", type=int, default=8770)
    args = parser.parse_args(argv)
    uvicorn.run(create_app(), host=args.host, port=args.port, proxy_headers=True, forwarded_allow_ips="127.0.0.1")


if __name__ == "__main__":
    main()
