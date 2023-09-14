import pytest
import os.path
import glob

DATADIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data', 'preprocessing'))

def test_dir_loc():
    assert os.path.isdir(DATADIR)
    print("Datadir: {} exists".format(DATADIR))
    xlsxfs = glob.glob("*.xlsx", root_dir=DATADIR)
    assert len(xlsxfs) == 1, "More than 1 xlsx file in test directory : {}. Please double check".format(xlsxfs)
    xlsxf =  os.path.join(DATADIR, xlsxfs[0])
    assert os.path.exists(xlsxf), "Path {} does not exist: ".format(xlsxf)

def test_loading():
    