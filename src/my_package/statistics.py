# python imports
from sklearn.linear_model import LinearRegression
import numpy as np
from numpy import cov
from scipy.stats import spearmanr
from scipy.stats import pearsonr


# calculate the covariance matrix between two variables
def covariance_matrix(x_value, y_value):
    covariance_matrix = cov(x_value, y_value)
    return covariance_matrix


# calculate the Pearson's correlation between two variables
def Pearson_correlation_coefficient(x_value, y_value):
    correlation, _ = pearsonr(x_value, y_value)
    return correlation


# calculate the spearmans's correlation between two variables
def spearman_correlation(x_value, y_value):
    correlation, _ = spearmanr(x_value, y_value)
    return correlation


def linear_regression_old(x_value, y_value):
    X = np.array(x_value).reshape(-1, 1)
    y = np.array(y_value).reshape(-1, 1)
    model = LinearRegression()
    reg = model.fit(X, y)
    return model, reg.intercept_, reg.coef_

def linear_regression(x_value, y_value):
    model = LinearRegression()
    reg = model.fit(x_value, y_value)
    return model, reg.intercept_, reg.coef_