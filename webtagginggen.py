#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import datetime
import fileinput

from doc_generator import find_pkg, repl_all

fingerprint_url = "http://ci.openmicroscopy.org/fingerprint"
MD5s = []


def usage():
    print "webtagginggen.py version"
    sys.exit(1)

try:
    version = sys.argv[1]
except:
    usage()

repl = {"@VERSION@": version,
        "@MONTHYEAR@": datetime.datetime.now().strftime("%b %Y")}

RSYNC_PATH = os.environ.get('RSYNC_PATH', '/ome/data_repo/public/')
PREFIX = os.environ.get('PREFIX', 'webtagging')
WEBTAGGING_RSYNC_PATH = '%s/%s/%s/' % (RSYNC_PATH, PREFIX, version)

repl["@ANNOUCEMENT_URL@"] = os.environ.get('ANNOUCEMENT_URL', forum_url)

for x, y in (
        ("WEBTAGGING", "webtagging-@VERSION@.zip"),
        ):

    find_pkg(repl, fingerprint_url, WEBTAGGING_RSYNC_PATH, x, y, MD5s)


for line in fileinput.input(["webtagging_downloads.html"]):
    print repl_all(repl, line, check_http=True),
