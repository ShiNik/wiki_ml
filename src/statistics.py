#user define imports

#python imports
from sklearn.linear_model import LinearRegression
import numpy as np
from numpy import cov
from scipy.stats import spearmanr
from scipy.stats import pearsonr

def covariance_matrix(x_value, y_value):
    # calculate the covariance matrix between two variables
    covariance_matrix = cov(x_value, y_value)
    return covariance_matrix

def Pearson_correlation_coefficient(x_value, y_value):
    # calculate the Pearson's correlation between two variables
    correlation, _ = pearsonr(x_value, y_value)
    return correlation

def spearman_correlation(x_value, y_value):
    # calculate the spearmans's correlation between two variables
    correlation, _ = spearmanr(x_value, y_value)
    return correlation

def linearRegression(x_value, y_value):
    X = np.array(x_value).reshape(-1, 1)
    y = np.array(y_value).reshape(-1, 1)
    reg = LinearRegression().fit(X, y)
    return reg.intercept_, reg.coef_

