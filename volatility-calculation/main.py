""" 
This code constitutes a submission for an assignment from a quant trading firm:
Given files containing price data for 4 stocks, calculate volatility
over the period as a percentage of annualised volatility of returns.

This submission is accompanied by a report and python notebook file.

Author: Ross Gales, 10/2/2023

"""

from os import listdir
from os.path import isfile, join

import pandas as pd
import numpy as np
from datetime import timedelta
import math


def remove_outliers(df, col, k=5, thresh=3):
    """
    Drops outliers rows from column col within thresh standard 
    deviations of k-neighbourhood median

    Parameters
    ----------
    df : pandas.Dataframe
        Dataframe for which the median is calculated.
    col : String
        Name of data column to calculate median from
    k : int
        size of neighbourhood from which median is calculated for each datum
    thresh : int
        number of standard deviations from the median above which rows are discarded


    Returns
    -------
    pandas.Dataframe
        Dataframe with outliers removed and enhanced with median and diff columns
    """

    # Select latest trade from each day as proxy for closing price:
    df = df.groupby(pd.Grouper(key='ts', axis=0, 
                      freq='1D', sort=True)).tail(1).dropna()
    df = df.reset_index()

    # Create new columns for k-neighbour median and absolute difference
    col_med = 'median_k'+str(k)
    col_diff = 'median_k'+str(k)+'_diff'
    df[col_med] = np.nan
    df[col_diff] = np.nan

    # Add median and diff values for each row to new columns
    for index, row in df.iterrows():

        min_i = max(index-k, 0)
        max_i = min(df.shape[0]-1, index+k)
        median = df.iloc[min_i:max_i+1][col].median()
        
        df.at[index,col_med] = median
        df.at[index,col_diff] = abs(median - df.iloc[index][col])
    
    # Drop outlier rows where difference is greater than: threshold * std
    df = df.loc[df[col_diff] < thresh * df[col_diff].std()]
    df = df.reset_index()

    return df



def calc_vol(df, col):
    """
    Calculate the annualised percentage volatility for column: col

    Parameters
    ----------
    df : pandas.Dataframe
        Dataframe for which the volatility is calculated. 
        Each row represents a daily price.
    col : String
        Name of data column for which volatility is calculated.

    Returns
    -------
    float
        Volatility measure as a decimal value
    """

    # Calculate percentage returns between rows
    df['return'] = np.nan
    for i, row in df.iterrows():
        if i == 0:
            continue
        df.at[i, 'return'] = df.iloc[i][col]/df.iloc[i-1][col]-1

    # Calculate annualised volatility
    vol = df['return'].std() * math.sqrt(252)
    return(vol)





if __name__ == "__main__":

    # Stand in code for data input, in place of pipeline integration:
    data_path = 'prices'
    files = [f for f in listdir(data_path) if isfile(join(data_path, f))]

    for f in files:
        df = pd.read_csv(join(data_path, f), parse_dates=[0])
        
        #######################
        ## Start of Pipeline ##

        # Remove outliers (values outside 3 standard 
        # deviations of 5-point neighbourhood)
        df = remove_outliers(df, 'price')

        # Calculate annualised daily volatility of returns
        vol = calc_vol(df, 'price')

        ### End of pipeline ###
        #######################

        # Stand in code for output, in place of pipeline integration:
        print('Volatility for stock {} = {:.4}%'.format(f, vol*100))
