#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Benjamin Vial
# This file is part of pyonelab
# License: MIT

import os
import importlib.metadata as metadata
import platform


def get_meta(metadata):
    data = metadata.metadata("pyonelab")
    __version__ = metadata.version("pyonelab")
    __author__ = data.get("author")
    __description__ = data.get("summary")
    return __version__, __author__, __description__


__version__, __author__, __description__ = get_meta(metadata)

_getdp_name = "getdp"
_gmsh_name = "getdp"
if platform.system() == "Windows":
    _getdp_name += ".exe"
    _gmsh_name += ".exe"
getdp_exec_path = os.path.join(os.path.dirname(__file__), "bin", _getdp_name)
gmsh_exec_path = os.path.join(os.path.dirname(__file__), "bin", _gmsh_name)
