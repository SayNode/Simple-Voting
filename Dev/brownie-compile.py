#!/usr/bin/python3

import shutil

from brownie import project
from brownie._config import _load_project_structure_config
from brownie.exceptions import ProjectNotFound
from brownie.utils import color
from brownie.utils.docopt import docopt

CODESIZE_COLORS = [(1, "bright red"), (0.8, "bright yellow")]

__doc__ = """Usage: brownie compile [<contract> ...] [options]
Arguments
  [<contract> ...]       Optional list of contract names to compile.
Options:
  --all -a              Recompile all contracts
  --size -s             Show deployed bytecode sizes contracts
  --help -h             Display this message
Compiles the contract source files for this project and saves the results
in the build/contracts/ folder.
Note that Brownie automatically recompiles any changed contracts each time
a project is loaded. You do not have to manually trigger a recompile."""


def main():
    project_path = project.check_for_project(".")
    print(project_path)

    if project_path is None:
        raise ProjectNotFound

    build_path = project_path.joinpath(_load_project_structure_config(project_path)["build"])

    contract_artifact_path = build_path.joinpath("contracts")
   
    interface_artifact_path = build_path.joinpath("interfaces")


    shutil.rmtree(contract_artifact_path, ignore_errors=True)
    shutil.rmtree(interface_artifact_path, ignore_errors=True)


    proj = project.load()



    print(f"Project has been compiled. Build artifacts saved at {contract_artifact_path}")

main()