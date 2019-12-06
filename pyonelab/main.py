"""
Tools for gmsh/getdp control and input/output.

"""

import os
import shutil
import platform

_system = platform.system()

_script_path = os.path.realpath(os.path.dirname(os.path.abspath(__file__)))
_bin_path = os.path.realpath(os.path.join(_script_path, "bin", _system))
_local_folder_exist = os.path.exists(_bin_path)

print("_local_folder_exist: ", _local_folder_exist)

gmsh = shutil.which("gmsh")
getdp = shutil.which("getdp")


def _download_onelab():
    script_path = os.path.realpath(
        os.path.join(_script_path, "scripts", "install_onelab_prebuilt.sh")
    )
    bash_cmd = "bash {0} {1} {2} {3}".format(script_path, _system, _bin_path, "stable")
    os.system(bash_cmd)


if getdp == None or gmsh == None:
    _local_folder_exist = os.path.exists(_bin_path)
    if _local_folder_exist:
        # print("Local onelab already installed")
        pass
    else:
        print("Installing onelab on your system")
        _download_onelab()
else:
    pass
    # print("Found system onelab")


if gmsh is None:
    gmsh = os.path.realpath(os.path.join(_bin_path, "gmsh"))
if getdp is None:
    getdp = os.path.realpath(os.path.join(_bin_path, "getdp"))


# def load_data():
#     if not os.path.exists(DATA_DIR):
#         download_data()
#     data = read_data_from_disk(DATA_DIR)
#     return data
