#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Benjamin Vial
# This file is part of pyonelab
# License: MIT

import sys
import os
import shutil
import urllib.request
import tarfile
import zipfile
import tempfile

import logging
logger = logging.getLogger(__name__)

OS = sys.argv[1]
ONELAB_PATH = os.path.realpath(sys.argv[2])
VERSION = sys.argv[3]

if VERSION == "stable":
    GMSH_VERSION = "4.13.1"
    GETDP_VERSION = "3.5.0"
elif VERSION == "dev":
    GMSH_VERSION = "git"
    GETDP_VERSION = "git"
else:
    sys.exit(1)

os.makedirs(ONELAB_PATH, exist_ok=True)
os.chdir(ONELAB_PATH)

logger.info("Installing onelab {} for {} in {}".format(VERSION, OS, ONELAB_PATH))

if OS == "Linux":
    EXTRACT = tarfile.open
    ARCHEXT = "tgz"
    GMSH_NAME = "gmsh-{}-Linux64".format(GMSH_VERSION)
    GMSH_ARCH = "Linux/{}.{}".format(GMSH_NAME, ARCHEXT)
    GETDP_NAME = "getdp-{}-Linux64".format(GETDP_VERSION)
    GETDP_ARCH = "Linux/{}c.{}".format(GETDP_NAME, ARCHEXT)

elif OS == "Darwin":
    EXTRACT = tarfile.open
    ARCHEXT = "tgz"
    GMSH_NAME = "gmsh-{}-MacOSX-sdk".format(GMSH_VERSION)
    GMSH_ARCH = "MacOSX/{}.{}".format(GMSH_NAME, ARCHEXT)
    GETDP_NAME = "getdp-{}-MacOSX".format(GETDP_VERSION)
    GETDP_ARCH = "MacOSX/{}c.{}".format(GETDP_NAME, ARCHEXT)

elif OS == "Windows":
    EXTRACT = zipfile.ZipFile
    ARCHEXT = "zip"
    GMSH_NAME = "gmsh-{}-Windows64".format(GMSH_VERSION)
    GMSH_ARCH = "Windows/{}.{}".format(GMSH_NAME, ARCHEXT)
    GETDP_NAME = "getdp-{}-Windows64".format(GETDP_VERSION)
    GETDP_ARCH = "Windows/{}c.{}".format(GETDP_NAME, ARCHEXT)


tmpdir = tempfile.mkdtemp()
os.chdir(tmpdir)


def extract_archive(archname):
    with EXTRACT(archname) as f:
        # f.extractall(filter="fully_trusted")
        f.extractall()

# gmsh

logger.info("Installing gmsh...")
with urllib.request.urlopen("https://gmsh.info/bin/{}".format(GMSH_ARCH)) as response:
    with open("gmsh.{}".format(ARCHEXT), "wb") as f:
        f.write(response.read())
extract_archive("gmsh.{}".format(ARCHEXT))

if OS == "windows":
    shutil.copy2(os.path.join(tmpdir, GMSH_NAME, "gmsh.exe"), ONELAB_PATH)
else:
    shutil.copy2(os.path.join(tmpdir, GMSH_NAME, "bin", "gmsh"), ONELAB_PATH)

if OS == "osx":
    for f in os.listdir("gmsh_tmp/lib"):
        if f.endswith(".dylib"):
            shutil.copy2(os.path.join(tmpdir, GMSH_NAME, "lib", f), ONELAB_PATH)


# getdp

logger.info("Installing getdp...")
with urllib.request.urlopen("https://getdp.info/bin/{}".format(GETDP_ARCH)) as response:
    with open("getdp.{}".format(ARCHEXT), "wb") as f:
        f.write(response.read())
extract_archive("getdp.{}".format(ARCHEXT))
if OS == "windows":
    shutil.copy2(os.path.join(tmpdir, GETDP_NAME, "getdp.exe"), ONELAB_PATH)
else:
    shutil.copy2(os.path.join(tmpdir, GETDP_NAME, "bin", "getdp"), ONELAB_PATH)


logger.info("Installation done.")
