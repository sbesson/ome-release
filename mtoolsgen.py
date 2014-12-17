#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import datetime
import fileinput

from doc_generator import find_pkg, repl_all


def usage():
    print "mtoolsgen.py version"
    sys.exit(1)

try:
    version = sys.argv[1]
except:
    usage()

repl = {"@VERSION@": version,
        "@MONTHYEAR@": datetime.datetime.now().strftime("%b %Y")}

RSYNC_PATH = os.environ.get('RSYNC_PATH', '/ome/data_repo/public/')
PREFIX = os.environ.get('PREFIX', 'mtools')
UTRACK_RSYNC_PATH = '%s/%s/%s/' % (RSYNC_PATH, PREFIX, version)

for x, y in (
        ("MTOOLS_WIN", "OMERO.mtools_@VERSION@_win.zip"),
        ("MTOOLS_MAC", "OMERO.mtools_@VERSION@_mac.zip"),
        ):

    find_pkg(repl, UTRACK_RSYNC_PATH, x, y)

for line in fileinput.input(["mtools_downloads.html"]):
    print repl_all(repl, line, check_http=True),
