"""Module containing models representing lightcurves.

The Model layer is responsible for the 'business logic' part of the software.

The lightcurves are saved in a table (2D array) where each row corresponds to a single observation. 
Depending on the dataset (LSST or Kepler), 
a table can contain observations of a single or several objects, 
in a single or different bands.

Functions:
    load_dataset
    mean_mag
    max_mag
    min_mag
"""

import pandas as pd
from astropy.timeseries import LombScargle


def load_dataset(filename):
    """Load a table from CSV file.
    :param filename: The name of the .csv file to load
    :returns: pd.DataFrame with the data from the file.
    """
    return pd.read_csv(filename)


def mean_mag(data, mag_col):
    """Calculate the mean magnitude of a lightcurve
    :param data: pd.DataFrame with observed magnitudes for a single source.
    :param mag_col: a string with the name of the column for calculating the mean value.
    :returns: The mean value of the column
    """
    return data[mag_col].mean()


def max_mag(data, mag_col):
    """Calculate the max magnitude of a lightcurve
    :param data: pd.DataFrame with observed magnitudes for a single source.
    :param mag_col: a string with the name of the column for calculating the max value.
    :returns: The max value of the column
    """
    return data[mag_col].max()


def min_mag(data, mag_col):
    """Calculate the min magnitude of a lightcurve
    :param data: pd.DataFrame with observed magnitudes for a single source.
    :param mag_col: a string with the name of the column for calculating the min value.
    :returns: The min value of the column.
    """
    return data[mag_col].min()


def calc_stats(lc, bands, mag_col):
    """Calculate max, mean and min values for all bands of a light curve
    :param lc: Dictionary of pd.DataFrame with observed magnitudes for a single source.
    :param bands: a string with the magnitude band names.
    :param mag_col: a string with the name of the column for calculating the min value.
    :returns: pd.DataFrame with max, mean, and min values.
    """
    stats = {}
    for b in bands:
        stat = {}
        stat["max"] = max_mag(lc[b], mag_col)
        stat["mean"] = mean_mag(lc[b], mag_col)
        stat["min"] = min_mag(lc[b], mag_col)
        stats[b] = stat
    return pd.DataFrame.from_records(stats)


def normalize_lc(df, mag_col):
    """Normalize a light curve.
    :param df: pd.DataFrame with observed magnitudes for a single source.
    :param mag_col: a string with the name of the column for calculating the min value.
    :returns: pd.Series of normalized magnitude values.
    """
    if any(df[mag_col].abs() > 90):
        raise ValueError(mag_col + " contains values with abs() larger than 90!")
        
    min_data = min_mag(df, mag_col)
    max_data = max_mag((df - min_data), mag_col)
    lc = (df[mag_col] - min_data) / max_data
    lc = lc.fillna(0)
    return lc
