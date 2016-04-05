#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import datetime
import fileinput

from utils import RSYNC_PATH, get_version, get_tag_url
from doc_generator import find_pkg, repl_all


def usage():
    print "filescppgen.py version buildid"
    sys.exit(1)

try:
    files_version = sys.argv[1]
    buildid = sys.argv[2]
except:
    usage()

# Read major and minor version from input version
major_version, minor_version = get_version(files_version)

superbuild_version = '0.1.0'
common_version = '5.2.0-m2'
bf_version = '5.2.0-m2.5'
bf_major_version, bf_minor_version = get_version(bf_version)
qtwidgets_version = '5.2.0-m2'

repl = {"@VERSION@": files_version,
        "@BUILDID@": buildid,
        "@BF_VERSION@": bf_version,
        "@XML_VERSION@": bf_version,
        "@COMMON_VERSION@": common_version,
        "@FILES_VERSION@": files_version,
        "@QTWIDGETS_VERSION@": qtwidgets_version,
        "@SUPERBUILD_VERSION@": superbuild_version,
        "@MONTHYEAR@": datetime.datetime.now().strftime("%b %Y")}

repl["@SUPERBUILD_TAG_URL@"] = get_tag_url("ome-cmake-superbuild",
                                           superbuild_version,
                                           org="ome")
repl["@COMMON_TAG_URL@"] = get_tag_url("ome-common-cpp",
                                       common_version, org="ome")
repl["@XML_TAG_URL@"] = get_tag_url("bioformats", bf_version)
repl["@FILES_TAG_URL@"] = get_tag_url("ome-files-cpp",
                                      files_version, org="ome")
repl["@QTWIDGETS_TAG_URL@"] = get_tag_url("ome-qtwidgets",
                                          qtwidgets_version, org="ome")

repl["@DOC_URL@"] = (
    "../../docs/%s/ome-files/manual/html/"
    % (buildid))
repl["@COMMON_API_URL@"] = (
    "../../docs/%s/ome-common/api/html/"
    % (buildid))
repl["@XML_API_URL@"] = (
    "../../docs/%s/ome-xml/api/html/"
    % (buildid))
repl["@FILES_API_URL@"] = (
    "../../docs/%s/ome-files/api/html/"
    % (buildid))
repl["@QTWIDGETS_API_URL@"] = (
    "../../docs/%s/ome-qtwidgets/api/html/"
    % (buildid))

PREFIX = os.environ.get('PREFIX', 'ome-files-cpp')
FILESCPP_RSYNC_PATH = '%s/%s/%s/artifacts/%s/' % (RSYNC_PATH, PREFIX,
                                                  files_version, buildid)

# Links to Bio-Formats artifacts
RELATIVE_PATH = '../../../../'
ome_sources = [
    ("COMMON_SOURCE_TXZ", RELATIVE_PATH +
     ("ome-common-cpp/%s/source/" +
      "ome-common-cpp-%s.tar.xz") % (
          common_version, common_version)),
    ("COMMON_SOURCE_ZIP", RELATIVE_PATH +
     ("ome-common-cpp/%s/source/" +
      "ome-common-cpp-%s.zip") % (
          common_version, common_version)),
    ("BF_SOURCE_TXZ", RELATIVE_PATH +
     ("bio-formats/%s/artifacts/" +
      "bioformats-dfsg-%s.tar.xz") % (
          bf_version, bf_version)),
    ("BF_SOURCE_ZIP", RELATIVE_PATH +
     ("bio-formats/%s/artifacts/" +
      "bioformats-dfsg-%s.zip") % (
          bf_version, bf_version)),
    ("FILES_SOURCE_TXZ", RELATIVE_PATH +
     ("ome-files-cpp/%s/source/" +
      "ome-files-cpp-%s.tar.xz") % (
          files_version, files_version)),
    ("FILES_SOURCE_ZIP", RELATIVE_PATH +
     ("ome-files-cpp/%s/source/" +
      "ome-files-cpp-%s.zip") % (
          files_version, files_version)),
    ("QTWIDGETS_SOURCE_TXZ", RELATIVE_PATH +
     ("ome-qtwidgets/%s/source/" +
      "ome-qtwidgets-%s.tar.xz") % (
          qtwidgets_version, qtwidgets_version)),
    ("QTWIDGETS_SOURCE_ZIP", RELATIVE_PATH +
     ("ome-qtwidgets/%s/source/" +
      "ome-qtwidgets-%s.zip") % (
          qtwidgets_version, qtwidgets_version)),
    ("SUPERBUILD_SOURCE_TXZ", RELATIVE_PATH +
     ("ome-cmake-superbuild/%s/source/" +
      "ome-cmake-superbuild-%s.tar.xz") % (
          superbuild_version, superbuild_version)),
    ("SUPERBUILD_SOURCE_ZIP", RELATIVE_PATH +
     ("ome-cmake-superbuild/%s/source/" +
      "ome-cmake-superbuild-%s.zip") % (
          superbuild_version, superbuild_version))]

thirdparty_sources = {
    'TP_BF_SOURCE': 'bioformats-dfsg-5.2.0-m2.5.tar.xz',
    'BOOST_SOURCE': 'boost_1_60_0.tar.bz2',
    'BZIP2_SOURCE': 'bzip2-1.0.6.tar.gz',
    'PY_DOCUTILS_SOURCE': 'docutils-0.12.tar.gz',
    'PY_GENSHI_SOURCE': 'Genshi-0.7.tar.gz',
    'ICU_SOURCE': 'icu4c-55_1-src.tgz',
    'PY_JINJA2_SOURCE': 'Jinja2-2.7.3.tar.gz',
    'PNG_SOURCE': 'libpng-1.6.21.tar.xz',
    'PY_MARKUPSAFE_SOURCE': 'MarkupSafe-0.23.tar.gz',
    'TP_COMMON_SOURCE': 'ome-common-cpp-5.2.0-m2.tar.xz',
    'TP_FILES_SOURCE': 'ome-files-cpp-0.1.0.tar.xz',
    'TP_QTWIDGETS_SOURCE': 'ome-qtwidgets-5.2.0-m2.tar.xz',
    'PY_PYGMENTS_SOURCE': 'Pygments-2.0.2.tar.gz',
    'GTEST_SOURCE': 'release-1.7.0.tar.gz',
    'PY_SETUPTOOLS_SOURCE': 'setuptools-18.3.2.tar.gz',
    'PY_SPHINX_SOURCE': 'Sphinx-1.2.3.tar.gz',
    'TIFF_SOURCE': 'tiff-4.0.6.tar.gz',
    'XALAN_SOURCE': 'xalan_c-1.11-src.tar.gz',
    'XERCES_SOURCE': 'xerces-c-3.1.3.tar.xz',
    'ZLIB_SOURCE': 'zlib-1.2.8.tar.xz'}

# Links to Bio-Formats C++ artifacts
platforms = {'UBUNTU1404': 'Ubuntu14.04-x86_64',
             'OSX1011':    'MacOSX10.11-x86_64',
             'CENTOS67':   'CentOS6.7-x86_64',
             'CENTOS72':   'CentOS7.2-x86_64'}

win_platforms = {'WINDOWSVC12X64': 'VC12-x64',
                 'WINDOWSVC12X86': 'VC12-x86'}

build_types = ['Debug', 'Release']

files_cpp_artifacts = [
    ("DOXYGEN", "docs/ome-files-bundle-apidoc-@VERSION@.tar.xz")]

for platform in platforms.keys():
    for build_type in build_types:
        files_cpp_artifacts.append(
            ('%s_%s' % (platform, build_type.upper()),
             'binaries/' +
             'ome-files-standalone-bundle-@VERSION@-%s-%s-b%s.tar.xz'
             % (build_type, platforms[platform], buildid)))
for platform in win_platforms.keys():
    for build_type in build_types:
        files_cpp_artifacts.append(
            ('%s_%s' % (platform, build_type.upper()),
             'binaries/' +
             'ome-files-bundle-@VERSION@-%s-%s-b%s.zip'
             % (win_platforms[platform], build_type, buildid)))

files_cpp_platform_artifacts = list()
for platform in platforms.keys():
    for build_type in build_types:
        platform_artifact = \
            ('%sPLATFORM_%s' % (platform, build_type.upper()),
             'binaries/' +
             'ome-files-platform-bundle-@VERSION@-%s-%s-b%s.tar.xz'
             % (build_type, platforms[platform], buildid))
        try:
            find_pkg(repl, FILESCPP_RSYNC_PATH,
                     platform_artifact[0], platform_artifact[1])
            files_cpp_artifacts.append(platform_artifact)
        except:
            pass

for src in thirdparty_sources.keys():
    files_cpp_artifacts.append(
        (src,
         'sources/%s' % (thirdparty_sources[src])))

for x, y in ome_sources + files_cpp_artifacts:
    find_pkg(repl, FILESCPP_RSYNC_PATH, x, y)

for line in fileinput.input(["files_cpp_downloads.html"]):
    print repl_all(repl, line, check_http=True)
