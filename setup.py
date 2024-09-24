#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Benjamin Vial
# This file is part of pyonelab
# License: MIT

import shutil
import sys
import subprocess
from contextlib import suppress
from pathlib import Path
from setuptools import Command, setup
from setuptools.command.build import build
from setuptools import logging
import os
import platform


class CustomCommand(Command):
    def initialize_options(self) -> None:
        self.bdist_dir = None
        self.pkg_name = None

    def finalize_options(self) -> None:
        self.pkg_name = self.distribution.get_name().replace("-", "_")
        with suppress(Exception):
            self.bdist_dir = Path(self.get_finalized_command("bdist_wheel").bdist_dir)

    def run(self) -> None:
        logging.logging.info("Downloading binaries")
        system = platform.system()
        script_path = os.path.realpath(os.path.dirname(os.path.abspath(__file__)))
        bin_path = os.path.realpath(os.path.join(script_path, self.pkg_name, "bin"))
        lib_path = os.path.realpath(os.path.join(script_path, self.pkg_name, "lib"))
        onelab_version = "stable"
        command = [
            "python",
            "dev/install_onelab_prebuilt.py",
            system,
            bin_path,
            lib_path,
            onelab_version,
        ]
        if subprocess.call(command) != 0:
            sys.exit(-1)
        logging.logging.info(f"Copied binary files {os.listdir(bin_path)}")
        logging.logging.info(f"Copied lib files {os.listdir(lib_path)}")


class CustomBuild(build):
    sub_commands = [("build_custom", None)] + build.sub_commands


setup(
    cmdclass={
        "build": CustomBuild,
        "build_custom": CustomCommand,
    },
    scripts=["pyonelab/gmsh", "pyonelab/getdp"],
    # package_data={"pyonelab": ["bin/*"]},
)
