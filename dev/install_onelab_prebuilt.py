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

logger.info(f"Installing onelab {VERSION} for {OS} in {ONELAB_PATH}")

if OS == "Linux":
    EXTRACT = tarfile.open
    ARCHEXT = "tgz"
    GMSH_NAME = f"gmsh-{GMSH_VERSION}-Linux64"
    GMSH_ARCH = f"Linux/{GMSH_NAME}.{ARCHEXT}"
    GETDP_NAME = f"getdp-{GETDP_VERSION}-Linux64"
    GETDP_ARCH = f"Linux/{GETDP_NAME}c.{ARCHEXT}"

elif OS == "Darwin":
    EXTRACT = tarfile.open
    ARCHEXT = "tgz"
    GMSH_NAME = f"gmsh-{GMSH_VERSION}-MacOSX-sdk"
    GMSH_ARCH = f"MacOSX/{GMSH_NAME}.{ARCHEXT}"
    GETDP_NAME = f"getdp-{GETDP_VERSION}-MacOSX"
    GETDP_ARCH = f"MacOSX/{GETDP_NAME}c.{ARCHEXT}"

elif OS == "Windows":
    EXTRACT = zipfile.ZipFile
    ARCHEXT = "zip"
    GMSH_NAME = f"gmsh-{GMSH_VERSION}-Windows64"
    GMSH_ARCH = f"Windows/{GMSH_NAME}.{ARCHEXT}"
    GETDP_NAME = f"getdp-{GETDP_VERSION}-Windows64"
    GETDP_ARCH = f"Windows/{GETDP_NAME}c.{ARCHEXT}"

tmpdir = tempfile.mkdtemp()
os.chdir(tmpdir)


def extract_archive(archname):
    with EXTRACT(archname) as f:
        # f.extractall(filter="fully_trusted")
        f.extractall()

# gmsh

logger.info(f"Installing gmsh...")
with urllib.request.urlopen(f"https://gmsh.info/bin/{GMSH_ARCH}") as response:
    with open(f"gmsh.{ARCHEXT}", "wb") as f:
        f.write(response.read())
extract_archive(f"gmsh.{ARCHEXT}")

if OS == "windows":
    shutil.copy2(os.path.join(tmpdir, GMSH_NAME, "gmsh.exe"), ONELAB_PATH)
else:
    shutil.copy2(os.path.join(tmpdir, GMSH_NAME, "bin", "gmsh"), ONELAB_PATH)

if OS == "osx":
    for f in os.listdir(os.path.join(tmpdir, GMSH_NAME, "lib")):
        if f.endswith(".dylib"):
            shutil.copy2(os.path.join(tmpdir, GMSH_NAME, "lib", f), ONELAB_PATH)


# getdp

logger.info(f"Installing getdp...")
with urllib.request.urlopen(f"https://getdp.info/bin/{GETDP_ARCH}") as response:
    with open(f"getdp.{ARCHEXT}", "wb") as f:
        f.write(response.read())
extract_archive(f"getdp.{ARCHEXT}")
if OS == "windows":
    shutil.copy2(os.path.join(tmpdir, GETDP_NAME, "getdp.exe"), ONELAB_PATH)
else:
    shutil.copy2(os.path.join(tmpdir, GETDP_NAME, "bin", "getdp"), ONELAB_PATH)


logger.info("Installation done.")

