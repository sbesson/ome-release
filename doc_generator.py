#!/usr/bin/env venv/bin/python
# -*- coding: utf-8 -*-


import os
import glob

from urllib2 import build_opener, Request

FINGERPRINT_URL = os.environ.get(
    'FINGERPRINT_URL', "http://ci.openmicroscopy.org/fingerprint")


class HeadRequest(Request):
    """Subclass of urllib2.Request that sends a HEAD request."""
    def get_method(self):
        return 'HEAD'


# create an opener that will simulate a browser user-agent
opener = build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]


class Filesize(object):
    """
    Container for a size in bytes with a human readable representation
    Use it like this::

        >>> size = Filesize(123123123)
        >>> print size

        '117.4 MB'

    See: http://stackoverflow.com/questions/1094841/\
    reusable-library-to-get-human-readable-version-of-file-size
    """

    chunk = 1024
    units = ['bytes', 'KB', 'MB', 'GB', 'TB', 'PB']
    precisions = [0, 0, 1, 2, 2, 2]

    def __init__(self, size):
        self.size = size

    def __int__(self):
        return self.size

    def __str__(self):
        if self.size == 0:
            return '0 bytes'
        from math import log
        unit = self.units[min(int(log(self.size, self.chunk)),
                          len(self.units) - 1)]
        return self.format(unit)

    def format(self, unit):
        if unit not in self.units:
            raise Exception("Not a valid file size unit: %s" % unit)
        if self.size == 1 and unit == 'bytes':
            return '1 byte'
        exponent = self.units.index(unit)
        quotient = float(self.size) / self.chunk**exponent
        precision = self.precisions[exponent]
        format_string = '{:.%sf} {}' % (precision)
        return format_string.format(quotient, unit)


def check_url(url):
    """
    Check if a URL exists without downloading the whole file.
    We only check the URL header.
    See https://bitbucket.org/birkenfeld/sphinx/src/\
    a5c993967b40682227b7d8a54073c6155d9e11b5/sphinx/builders/\
    linkcheck.py?at=stable
    """

    # need to actually check the URI
    try:
        f = opener.open(HeadRequest(url))
        f.close()
    except Exception, err:
        return 'broken', str(err)
    if f.url.rstrip('/') == url.rstrip('/'):
        return 'working', f.url
    else:
        return 'redirected', f.url


def get_hash(filename, type):

    read_hash = None
    with open(filename + '.' + type, "r") as f:
        read_hash = f.read().rsplit()[0]
    return read_hash


def repl_all(repl, line, check_http=False):
    for k, v in repl.items():
        line = line.replace(k, v)
    if False:  # check_http:
        for part in line.split():
            if part.startswith("href=") and not part[6] == '/':
                part = part[6:]
                url = part[0: part.find('"')]
                [status, info] = check_url(url)
                if not status == 'working' and not status == 'redirected':
                    raise Exception("%s: %s" % (url, info))
    return line


suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']


def humansize(nbytes):
    # See http://stackoverflow.com/questions/14996453
    if nbytes == 0:
        return '0 B'
    i = 0
    while nbytes >= 1000 and i < len(suffixes)-1:
        nbytes /= 1000.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])


def find_artifact(snapshot_path, path, ignore_md5=[]):
    """
    Mutates the repl argument
    """
    # path = repl_all(repl, path)
    rv = glob.glob(snapshot_path + path)
    d = {}
    d['path'] = path
    if len(rv) != 1:
        raise Exception("Results!=1 for %s: %s" % (snapshot_path + path, rv))
    fullpath = rv[0]

    d['md5'] = get_hash(fullpath, 'md5')
    d['sha1'] = get_hash(fullpath, 'sha1')
    d['size'] = os.path.getsize(fullpath)
    d['humansize'] = humansize(d['size'])
    d['name'] = os.path.basename(path)
    if "SKIP_MD5" not in os.environ and d['md5'] not in ignore_md5:
        furl = "/".join([FINGERPRINT_URL, d['md5'], "api", "xml"])
        if not check_url(furl):
            raise Exception("Error accessing %s for %s" % (furl, path))
    return d
