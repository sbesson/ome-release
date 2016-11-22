#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import datetime
import fileinput

from utils import RSYNC_PATH
from doc_generator import find_pkg, repl_all


def usage():
    print "utrackgen.py version"
    sys.exit(1)


try:
    version = sys.argv[1]
except:
    usage()

repl = {"@VERSION@": version,
        "@MONTHYEAR@": datetime.datetime.now().strftime("%b %Y"),
        "@YEAR@": datetime.datetime.now().strftime("%Y")}

PREFIX = os.environ.get('PREFIX', 'u-track')
UTRACK_RSYNC_PATH = '%s/%s/%s/' % (RSYNC_PATH, PREFIX, version)

for x, y in (
        ("SOURCE_CODE", "artifacts/u-track-@VERSION@.zip"),
        ("DOC", "artifacts/u-track-@VERSION@.pdf"),
        ):

    find_pkg(repl, UTRACK_RSYNC_PATH, x, y)

for line in fileinput.input(["utrack_downloads.html"]):
    print repl_all(repl, line, check_http=True),
