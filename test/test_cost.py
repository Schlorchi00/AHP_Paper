import pytest 
import os.path

DATADIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data', 'cost_calc'))

def test_dir_loc():
    assert os.path.isdir(DATADIR)
    print("Datadir: {} exists".format(DATADIR))