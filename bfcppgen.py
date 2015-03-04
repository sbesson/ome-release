#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import datetime
import fileinput

from utils import RSYNC_PATH, get_version, get_tag_url
from doc_generator import find_pkg, repl_all


def usage():
    print "bfcppgen.py version"
    sys.exit(1)

try:
    version = sys.argv[1]
except:
    usage()

repl = {"@VERSION@": version,
        "@MONTHYEAR@": datetime.datetime.now().strftime("%b %Y")}

# Read major and minor version from input version
major_version, minor_version = get_version(version)

repl["@TAG_URL@"] = get_tag_url("bioformats", version)
repl["@DOC_URL@"] = (
    "http://www.openmicroscopy.org/site/support/bio-formats%s.%s"
    % (major_version, minor_version))

PREFIX = os.environ.get('PREFIX', 'bio-formats-cpp')
BFCPP_RSYNC_PATH = '%s/%s/%s/' % (RSYNC_PATH, PREFIX, version)

# Links to Bio-Formats artifacts
BF_RELATIVE_PATH = '../../bio-formats/@VERSION@/artifacts/'
bf_artifacts = [
    ("DOC", BF_RELATIVE_PATH + "/Bio-Formats-@VERSION@.pdf"),
    ("SOURCE_CODE", BF_RELATIVE_PATH + "bioformats-@VERSION@.zip")]

# Links to Bio-Formats C++ artifacts
platforms = {'OSX108': 'MacOSX10.8',
             'CENTOS65': 'CentOS6.5-x86_64',
             'FREEBSD': 'FreeBSD10.1-RELEASE-x86_64'}
build_types = ['Debug', 'Release']

bf_cpp_artifacts = []
for platform in platforms.keys():
    for build_type in build_types:
        bf_cpp_artifacts.append(
            ('%s_%s' % (platform, build_type.upper()),
             'artifacts/bioformats-cpp-@VERSION@-%s-%s.tar.xz'
             % (build_type, platforms[platform])))

for x, y in bf_artifacts + bf_cpp_artifacts:
    find_pkg(repl, BFCPP_RSYNC_PATH, x, y)


for line in fileinput.input(["bf_cpp_downloads.html"]):
    print repl_all(repl, line, check_http=True),
