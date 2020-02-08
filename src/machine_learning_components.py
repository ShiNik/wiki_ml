# user define imports
import src.statistics as statistics
from src.analysis_info import ResultsInfo

# python imports
import numpy as np
import re


class MachineLearningComponents:
    def __init__(self):
        return


class LinearRegression(MachineLearningComponents):
    def __init__(self):
        return

    @staticmethod
    def perform_analysis(analysis):
        x_value = analysis.data_info.x_values
        y_value = analysis.data_info.y_values
        x = np.array(x_value)
        y = np.array(y_value)
        results_info = ResultsInfo()

        results_info.intercept, results_info.coef = statistics.linearRegression(x_value, y_value)

        # find the relationship
        results_info.covariance_matrix = statistics.covariance_matrix(x_value, y_value)

        # to find strength we use pearson correlation coefficient
        results_info.Pearson_correlation_coefficient = statistics.Pearson_correlation_coefficient(x_value, y_value)

        # Two  variables may be related by a nonlinear relationship
        results_info.spearman_correlation = statistics.spearman_correlation(x_value, y_value)
        analysis.results_info = results_info
