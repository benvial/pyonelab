#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Benjamin Vial
# This file is part of pyonelab
# License: MIT


import pyonelab
import subprocess
import platform


def test_getdp():
    exe_name = "getdp"
    if platform.system() == "Windows":
        exe_name += ".exe"
    out = subprocess.call([exe_name, "--info"], shell=True)
    assert out == 0
    out = subprocess.call([pyonelab.getdp_exec_path, "--version"], shell=True)
    assert out == 0
