#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Benjamin Vial
# This file is part of pyonelab
# License: MIT


import pyonelab
import subprocess


def test_getdp():
    out = subprocess.call(["getdp", "--info"])
    assert out == 0
    out = subprocess.call([pyonelab.gmsh_exec_path, "--version"])
    assert out == 0
