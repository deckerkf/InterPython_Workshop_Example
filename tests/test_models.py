"""Tests for statistics functions within the Model layer."""

import pandas as pd
import pytest
import numpy as np

def test_max_mag_integers():
    # Test that max_mag function works for integers
    from lcanalyzer.models import max_mag

    test_input_df = pd.DataFrame(data=[[1, 5, 3], 
                                       [7, 8, 9], 
                                       [3, 4, 1]], columns=list("abc"))
    test_input_colname = "a"
    test_output = 7

    assert max_mag(test_input_df, test_input_colname) == test_output

def test_max_mag_zeros():
    # Test that max_mag function works for zeros
    from lcanalyzer.models import max_mag

    test_input_df = pd.DataFrame(data=[[0, 0, 0], 
                                       [0, 0, 0], 
                                       [0, 0, 0]], columns=list("abc"))
    test_input_colname = "b"
    test_output = 0

    assert max_mag(test_input_df, test_input_colname) == test_output

def test_min_mag_integers():
    # Test that max_mag function works for integers
    from lcanalyzer.models import min_mag

    test_input_df = pd.DataFrame(data=[[1, 5, 3], 
                                       [7, 8, 9], 
                                       [3, 4, 1]], columns=list("abc"))
    test_input_colname = "a"
    test_output = 1

    assert min_mag(test_input_df, test_input_colname) == test_output


def test_max_mag_strings():
    # Test for TypeError when passing a string
    from lcanalyzer.models import max_mag

    test_input_colname = "b"
    with pytest.raises(TypeError):
        error_expected = max_mag('string', test_input_colname)

rng = np.random.default_rng(seed=42)
df1 = pd.DataFrame(rng.random((3, 3)), columns=list("abc"))
output1 = np.max(df1['b'])

@pytest.mark.parametrize(
    "test_df, test_colname, expected",
    [
        (pd.DataFrame(data=[[1, 5, 3], 
                            [7, 8, 9], 
                            [3, 4, 1]], 
                      columns=list("abc")),
        "a",
        7),
        (pd.DataFrame(data=[[0, 0, 0], 
                            [0, 0, 0], 
                            [0, 0, 0]], 
                      columns=list("abc")),
        "b",
        0),
        (df1,
         "b",
         pytest.approx(output1,0.01))
    ])
def test_max_mag(test_df, test_colname, expected):
    """Test max function works for array of zeroes, positive integers, and random floats."""
    from lcanalyzer.models import max_mag
    assert max_mag(test_df, test_colname) == expected