"""
Tools for gmsh/getdp control and input/output.

"""

import os
import shutil
import platform

system = platform.system()

script_path = os.path.dirname(os.path.abspath(__file__))
bin_path = os.path.join(script_path, "bin")

gmsh = shutil.which("gmsh")
getdp = shutil.which("getdp")
if gmsh is None:
    gmsh = os.path.join(bin_path, system, "gmsh")
if getdp is None:
    getdp = os.path.join(bin_path, system, "getdp")
