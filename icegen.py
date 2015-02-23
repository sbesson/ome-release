#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import datetime
import fileinput

from doc_generator import find_pkg, repl_all


def usage():
    print "icegen.py version build [source_suffix]"
    sys.exit(1)

try:
    version = sys.argv[1]
    build = sys.argv[2]
    if len(sys.argv) < 3:
        source_suffix = ""
    else:
        source_suffix = sys.argv[3]
except:
    usage()

repl = {"@VERSION@": version,
        "@BUILD@": build,
        "@SOURCE_SUFFIX@": source_suffix,
        "@MONTHYEAR@": datetime.datetime.now().strftime("%b %Y")}

RSYNC_PATH = os.environ.get('RSYNC_PATH', '/ome/data_repo/public/')
PREFIX = os.environ.get('PREFIX', 'ice')
ICE_RSYNC_PATH = '%s/%s/%s/' % (RSYNC_PATH, PREFIX, version)

for x, y in (
        ("ICE_X64_WIN",
         "artifacts/Ice-@VERSION@-@BUILD@-win-x64-Release.zip"),
        ("ICE_X86_WIN",
         "artifacts/Ice-@VERSION@-@BUILD@-win-x86-Release.zip"),
        ("SOURCE_CODE", "artifacts/Ice-@VERSION@.zip"),
        ("THIRD_PARTY",
         "artifacts/ThirdParty-Sources-@VERSION@@SOURCE_SUFFIX@.zip"),
        ):

    find_pkg(repl, ICE_RSYNC_PATH, x, y)


for line in fileinput.input(["ice_downloads.html"]):
    print repl_all(repl, line, check_http=True),
