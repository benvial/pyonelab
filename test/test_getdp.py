#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Benjamin Vial
# This file is part of pyonelab
# License: MIT


import pyonelab
import subprocess


def test_getdp():
    exe_name = "getdp"
    out = subprocess.call(["getdp", "--info"], shell=True)
    assert out == 0
    out = subprocess.call([pyonelab.getdp_exec_path, "--version"], shell=True)
    assert out == 0
