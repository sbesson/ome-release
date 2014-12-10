#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import datetime
import fileinput

from doc_generator import find_pkg, repl_all


def usage():
    print "gen.py version"
    sys.exit(1)

try:
    version = sys.argv[1]
except:
    usage()

repl = {"@VERSION@": version,
        "@MONTHYEAR@": datetime.datetime.now().strftime("%b %Y")}

RSYNC_PATH = os.environ.get('RSYNC_PATH', '/ome/data_repo/public/')
PREFIX = os.environ.get('PREFIX', 'ice')
ICE_RSYNC_PATH = '%s/%s/%s/' % (RSYNC_PATH, PREFIX, version)

for x, y in (
        ("ICE_X64_WIN", "Ice-@VERSION@-win-x64-Release.zip"),
        ("ICE_X86_WIN", "Ice-@VERSION@-win-x86-Release.zip"),
        ("SOURCE_CODE", "Ice-@VERSION@.zip"),
        ("THIRD_PARTY", "ThirdParty-Sources-@VERSION@.zip"),
        ):

    find_pkg(repl, ICE_RSYNC_PATH, x, y)


for line in fileinput.input(["ice_downloads.html"]):
    print repl_all(repl, line, check_http=True),
