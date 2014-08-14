#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import datetime
import fileinput

from doc_generator import find_pkg, repl_all

fingerprint_url = "http://ci.openmicroscopy.org/fingerprint"
daily_url = "http://ci.openmicroscopy.org/job/BIOFORMATS-5.1-daily/" \
    "lastSuccessfulBuild/artifact/artifacts"
latest_url = "http://ci.openmicroscopy.org/job/BIOFORMATS-5.1-latest/" \
    "lastSuccessfulBuild/artifact/artifacts"


def usage():
    print "bfgen.py version"
    sys.exit(1)

try:
    version = sys.argv[1]
except:
    usage()

repl = {"@VERSION@": version,
        "@MONTHYEAR@": datetime.datetime.now().strftime("%b %Y")}

MD5s = []

# Read major version from input version
import re
split_version = re.split("^([0-9]+)\.([0-9]+)\.([0-9]+)(.*?)$", version)
major_version = int(split_version[1])

# For calculating tags
import github
gh = github.Github()
ome = "openmicroscopy"
scc = "snoopycrimecop"
bf = "bioformats"

repo1 = gh.get_organization(ome).get_repo(bf)
repo2 = gh.get_user(scc).get_repo(bf)

for repo in (repo1, repo2):
    found = False
    for tag in repo.get_tags():
        if tag.name == ("v%s" % version):
            found = True
            break
    if found:
        break

repl["@TAG_URL@"] = repo.html_url + '/tree/' + tag.name
repl["@DOC_URL@"] = \
    "http://www.openmicroscopy.org/site/support/bio-formats%s" \
    % major_version

RSYNC_PATH = os.environ.get('RSYNC_PATH', '/ome/data_repo/public/')
PREFIX = os.environ.get('PREFIX', 'bio-formats')
BF_RSYNC_PATH = '%s/%s/%s/' % (RSYNC_PATH, PREFIX, version)

for x, y in (
        ("COMMAND_LINE_TOOLS", "artifacts/bftools.zip"),
        ("MATLAB_TOOLS", "artifacts/bfmatlab.zip"),
        ("DOC", "artifacts/Bio-Formats-@VERSION@.pdf"),
        ("JAVADOCS", "artifacts/bio-formats-javadocs.zip"),
        ("SOURCE_CODE", "artifacts/bioformats-@VERSION@.zip"),
        ("CPP_OSX109", "artifacts/bioformats-cpp-@VERSION@-MacOSX10.9.zip"),
        ("CPP_CENTOS65", "artifacts/bioformats-cpp-@VERSION@-CentOS6.5.zip"),
        ("bioformats_package.jar", "artifacts/bioformats_package.jar"),
        ("bio-formats_plugins.jar", "artifacts/bio-formats_plugins.jar"),
        ("bio-formats-testing-framework.jar",
         "artifacts/bio-formats-testing-framework.jar"),
        ("formats-api.jar", "artifacts/formats-api.jar"),
        ("formats-bsd.jar", "artifacts/formats-bsd.jar"),
        ("formats-bsd-test.jar", "artifacts/formats-bsd-test.jar"),
        ("formats-common.jar", "artifacts/formats-common.jar"),
        ("formats-gpl.jar", "artifacts/formats-gpl.jar"),
        ("jai_imageio.jar", "artifacts/jai_imageio.jar"),
        ("loci_tools.jar", "artifacts/loci_tools.jar"),
        ("lwf-stubs.jar", "artifacts/lwf-stubs.jar"),
        ("mdbtools-java.jar", "artifacts/mdbtools-java.jar"),
        ("metakit.jar", "artifacts/metakit.jar"),
        ("ome-xml.jar", "artifacts/ome-xml.jar"),
        ("ome-poi.jar", "artifacts/ome-poi.jar"),
        ("specification.jar", "artifacts/specification.jar"),
        ("turbojpeg.jar", "artifacts/turbojpeg.jar"),
        ):

    find_pkg(repl, fingerprint_url, BF_RSYNC_PATH, x, y, MD5s)

    repl["@DAILY_%s@" % x] = "%s/%s" % (daily_url, x)
    repl["@LATEST_%s@" % x] = "%s/%s" % (latest_url, x)

for line in fileinput.input(["bf_downloads.html"]):
    print repl_all(repl, line, check_http=True),
