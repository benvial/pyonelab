#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Benjamin Vial
# This file is part of pyonelab
# License: MIT

import pyonelab
import os
import subprocess
import tempfile
import platform

tempdir = tempfile.mkdtemp()


def test_gmsh():
    exe_name = "gmsh"
    if platform.system() == "Windows":
        exe_name += ".exe"
    out = subprocess.call([exe_name, "--info"], shell=True)
    assert out == 0
    out = subprocess.call([exe_name, "--version"], shell=True)
    assert out == 0
    out = subprocess.call([pyonelab.gmsh_exec_path, "--version"], shell=True)
    assert out == 0


t1 = """
// -----------------------------------------------------------------------------
//
//  Gmsh GEO tutorial 1
//
//  Geometry basics, elementary entities, physical groups
//
// -----------------------------------------------------------------------------

lc = 1e-2;

Point(1) = {0, 0, 0, lc};

Point(2) = {.1, 0,  0, lc};
Point(3) = {.1, .3, 0, lc};
Point(4) = {0,  .3, 0, lc};

Line(1) = {1, 2};
Line(2) = {3, 2};
Line(3) = {3, 4};
Line(4) = {4, 1};

Curve Loop(1) = {4, 1, -2, 3};

Plane Surface(1) = {1};

Physical Curve(5) = {1, 2, 4};
Physical Surface("My surface") = {1};

"""


def test_t1():
    geo = os.path.join(tempdir, "t1.geo")
    msh = os.path.join(tempdir, "t1.msh")
    with open(geo, "w") as f:
        f.write(t1)
    exe_name = "gmsh"
    if platform.system() == "Windows":
        exe_name += ".exe"
    out = subprocess.call([exe_name, geo, "-2", "-o", msh], shell=True)
    print(out)
    assert out == 0
    assert os.path.exists(msh)
