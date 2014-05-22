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
    print "gen.py version"
    sys.exit(1)

try:
    version = sys.argv[1]
except:
    usage()

repl = {"@VERSION@": version,
        "@MONTHYEAR@": datetime.datetime.now().strftime("%b %Y")}

# Read major version from input version
import re
split_version = re.split("^([0-9]+)\.([0-9]+)\.([0-9]+)(.*?)$", version)
major_version = int(split_version[1])

RSYNC_PATH = os.environ.get('RSYNC_PATH', '/ome/data_repo/public/')
PREFIX = os.environ.get('PREFIX', 'ice')
ICE_RSYNC_PATH = '%s/%s/%s/' % (RSYNC_PATH, PREFIX, version)

for x, y in (
        ("ICE_X64_WIN", "Ice-@VERSION@-win-x64-Release.zip"),
        ("ICE_X86_WIN", "Ice-@VERSION@-win-x84-Release.zip"),
        ("SOURCE_CODE", "Ice-@VERSION@.zip"),
        ("THIRD_PARTY", "ThirdParty-Sources-@VERSION@-1.zip"),
        ):

    find_pkg(repl, fingerprint_url, ICE_RSYNC_PATH, x, y, MD5s)


for line in fileinput.input(["ice_downloads.html"]):
    print repl_all(repl, line, check_http=True),
