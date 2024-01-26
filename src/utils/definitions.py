'''
Submodule to store and manage neccessary variables.
'''

from pathlib import Path

SRC_DIR = Path(__file__).parents[1]

ROOT_DIR = SRC_DIR.parent

DATA_DIR = ROOT_DIR.joinpath('data')

DB_FILE = DATA_DIR.joinpath('edb.db') # to be replaced by shared drive