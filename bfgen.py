#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import datetime
import fileinput

from utils import RSYNC_PATH, get_version, get_tag_url
from doc_generator import find_pkg, repl_all


def usage():
    print "bfgen.py version"
    sys.exit(1)

try:
    version = sys.argv[1]
except:
    usage()

repl = {"@VERSION@": version,
        "@MONTHYEAR@": datetime.datetime.now().strftime("%b %Y"),
        "@YEAR@": datetime.datetime.now().strftime("%Y")}

# Read major and minor version from input version
major_version, minor_version = get_version(version)

repl["@TAG_URL@"] = get_tag_url("bioformats", version)
repl["@DOC_URL@"] = (
    "http://www.openmicroscopy.org/site/support/bio-formats%s.%s"
    % (major_version, minor_version))

PREFIX = os.environ.get('PREFIX', 'bio-formats')
BF_RSYNC_PATH = '%s/%s/%s/' % (RSYNC_PATH, PREFIX, version)

for x, y in (
        ("COMMAND_LINE_TOOLS", "artifacts/bftools.zip"),
        ("MATLAB_TOOLS", "artifacts/bfmatlab.zip"),
        ("OCTAVE_PACKAGE", "artifacts/bioformats-octave-@VERSION@.tar.gz"),
        ("DOC", "artifacts/bio-formats-doc-@VERSION@.zip"),
        ("JAVADOCS", "artifacts/bio-formats-javadocs-@VERSION@.zip"),
        ("SOURCE_CODE_ZIP", "artifacts/bioformats-@VERSION@.zip"),
        ("SOURCE_CODE_TXZ", "artifacts/bioformats-@VERSION@.tar.xz"),
        ("bioformats_package.jar", "artifacts/bioformats_package.jar"),
        ("bio-formats_plugins.jar", "artifacts/bio-formats_plugins.jar"),
        ("bio-formats-testing-framework.jar",
         "artifacts/bio-formats-testing-framework.jar"),
        ("formats-api.jar", "artifacts/formats-api.jar"),
        ("formats-bsd.jar", "artifacts/formats-bsd.jar"),
        ("formats-gpl.jar", "artifacts/formats-gpl.jar"),
        ("jai_imageio.jar", "artifacts/jai_imageio.jar"),
        ("loci_tools.jar", "artifacts/loci_tools.jar"),
        ("turbojpeg.jar", "artifacts/turbojpeg.jar"),
        ):

    find_pkg(repl, BF_RSYNC_PATH, x, y)

for line in fileinput.input(["bf_downloads.html"]):
    print repl_all(repl, line, check_http=True),
