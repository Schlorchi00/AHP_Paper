import pytest
import os.path
import glob
import pandas as pd

from ahp.preprocessing import create_df, get_scaling, apply_linear_scaling, apply_scaling, apply_quadratic_scaling, empty_scaling

DATADIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data', 'preprocessing'))

def getfile() -> str:
    xlsxfs = glob.glob("*.xlsx", root_dir=DATADIR)
    xlsxf =  os.path.join(DATADIR, xlsxfs[0])
    return xlsxf

def getscaling() -> pd.DataFrame:
    xf = getfile()
    scale_df = get_scaling(xf)
    return scale_df

def test_dir_loc() -> str:
    assert os.path.isdir(DATADIR)
    print("Datadir: {} exists".format(DATADIR))
    xlsxfs = glob.glob("*.xlsx", root_dir=DATADIR)
    assert len(xlsxfs) == 1, "More than 1 xlsx file in test directory : {}. Please double check".format(xlsxfs)
    xlsxf =  os.path.join(DATADIR, xlsxfs[0])
    assert os.path.exists(xlsxf), "Path {} does not exist: ".format(xlsxf)
    # if not os.path.exists(xlsxf): pytest.exit("File for testing does not exist. Discontinuing")

def test_loading():
    xlsf = getfile()
    df, n_name = create_df(xlsf)
    assert isinstance(df, pd.DataFrame), "not a Dataframe. Double check"
    assert isinstance(n_name, str), "Name not a string. Doubel check"

def test_linear_scaling():
    """
        Function to test if the linear scaling produces consistent outputs
        e.g. -> run and then test consistency afterwards
    """
    xlsf = getfile()
    df, n_name = create_df(xlsf)
    scaling = get_scaling()

def test_quadrat_scaling():
    """
        Function to test if the quadratic scaling procudes consistent outputs. 
    """
    xlsf = getfile()
    df, n_name = create_df(xlsf)
    scaling = get_scaling()

def test_empty_scaling():
    """
        Function to test if the empty scaling produces consistent outputs. 
    """
    xlsf = getfile()
    df, n_name = create_df(xlsf)
    scaling = get_scaling()


def test_scaling_settings_quad():
    """
        Test if actually the quadratic settings get applied when setting the right places NA
    """
    xlsf = getfile()
    df, n_name = create_df(xlsf)
    scaling = get_scaling()

def test_scaling_settings_lin():
    """
        Test if actually the linear settings get applied when settings the right places NA
    """
    xlsf = getfile()
    df, n_name = create_df(xlsf)
    scaling = get_scaling()
    
    

