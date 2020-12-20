#!/usr/bin/env python
"""
NAME:

  mc-uuid-lookup:

DESCRIPTION:


AUTHOR:

  Jud Dagnall <jdagnall@splunk.com>

EXAMPLES:

    # common usage:
    mc-uuid-lookup 

"""

from __future__ import print_function

import argparse
import json
import logging
import requests
import sys

TIMESTAMP_FORMAT='%(asctime)s %(levelname)s - %(message)s'

def parse_args(args=None):
    desc=""
    p = argparse.ArgumentParser(description=desc)
    #p.add_argument('', help="default: %(default)s", default='')
    p.add_argument('-d', '--debug', action='store_true',
            help='turn on debug logging')
    p.add_argument('-m', '--max', default=None,
            type=int,
            help="max number of usernames to include. Default=all")
    p.add_argument("uuids", nargs="+", help="uuids to look up")
    # accept arguments as a param, so we
    # can import and run this module with a commandline-like
    # syntax.
    if args is None: 
        args = sys.argv[1:]
    return p.parse_args(args)

def run(opts):
    logging.debug("starting")
    for uuid in opts.uuids:
        url=f"https://api.mojang.com/user/profiles/{uuid}/names"
        result = requests.get(url).json() 
        names = [e['name'] for e in reversed(result)]
        if opts.max:
            names = names[:opts.max]
        print(uuid + "\t" + "|".join(names))

if __name__ == '__main__':
    opts = parse_args(sys.argv[1:])
    level = logging.DEBUG if opts.debug else logging.INFO
    logging.basicConfig(level=level,format=TIMESTAMP_FORMAT)
    run(opts)
