#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import datetime
import fileinput

from doc_generator import find_pkg, repl_all

fingerprint_url = "http://ci.openmicroscopy.org/fingerprint"


def usage():
    print "utrackgen.py version"
    sys.exit(1)

try:
    version = sys.argv[1]
except:
    usage()

repl = {"@VERSION@": version,
        "@MONTHYEAR@": datetime.datetime.now().strftime("%b %Y")}

MD5s = []


RSYNC_PATH = os.environ.get('RSYNC_PATH', '/ome/data_repo/public/')
PREFIX = os.environ.get('PREFIX', 'u-track')
UTRACK_RSYNC_PATH = '%s/%s/%s/' % (RSYNC_PATH, PREFIX, version)

for x, y in (
        ("SOURCE_CODE", "artifacts/U-Track-@VERSION@.zip"),
        ("DOC", "artifacts/U-Track-@VERSION@.pdf"),
        ):

    find_pkg(repl, fingerprint_url, UTRACK_RSYNC_PATH, x, y, MD5s)

for line in fileinput.input(["utrack_downloads.html"]):
    print repl_all(repl, line, check_http=True),
