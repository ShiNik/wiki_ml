# user define imports
from my_package import statistics as statistics
from my_package.analysis_info import ResultsInfo

# python imports
import numpy as np


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

        x_train = None
        y_train = None
        x_test = None
        if analysis.data_info.x_train is None:
            x_train = np.array(x_value).reshape(-1, 1)
            y_train = np.array(y_value).reshape(-1, 1)
            x_test = x_train
        else:
            x_train = analysis.data_info.x_train
            y_train = analysis.data_info.y_train
            x_test = analysis.data_info.x_test
            import pandas as pd
            df = pd.DataFrame({'x_train': x_train.flatten(), 'y_tain': y_train.flatten()})
            x_value = df['x_train'].to_numpy()
            y_value = df['y_tain'].to_numpy()

        results_info.model, results_info.intercept, results_info.coefficient = statistics.linear_regression(x_train, y_train)

        results_info.prediction = results_info.model.predict(x_test)

        # find the relationship
        results_info.covariance_matrix = statistics.covariance_matrix(x_value, y_value)

        # to find strength we use pearson correlation coefficient
        results_info.Pearson_correlation_coefficient = statistics.Pearson_correlation_coefficient(x_value, y_value)

        # Two  variables may be related by a nonlinear relationship
        results_info.spearman_correlation = statistics.spearman_correlation(x_value, y_value)
        analysis.results_info = results_info
