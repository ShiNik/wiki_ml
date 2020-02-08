class DataInfo:
    def __init__(self, x_data_info, y_data_info):
        self.x_values = x_data_info["values"]
        self.x_label = x_data_info["label"]
        self.y_values = y_data_info["values"]
        self.y_label = y_data_info["label"]


class ResultsInfo:
    def __init__(self):
        self.intercept = None
        self.coefficient = None
        self.covariance_matrix = None
        self.Pearson_correlation_coefficient = None
        self.spearman_correlation = None

    def get_eq_line(self):
        intercept = list(map('{:.3f}'.format, self.intercept))[0]
        coefficient = list(map('{:.3f}'.format, self.coefficient[0]))[0]
        eq_line = "Y = " + coefficient + " * X + " + intercept
        return eq_line

     # todo: is it necessary to pass in type param here
    def print(self, type):
        print("intercept: ", self.intercept, ", coefficient: ", self.coefficient)
        print(self.covariance_matrix)
        print("Pearson_correlation_coefficient: ", self.Pearson_correlation_coefficient)
        print("spearman_correlation: ", self.spearman_correlation)


class AnalysisInfo:
    def __init__(self, data_info, type):
        self.data_info = data_info
        self.results_info = None
        self.type = type

    def print(self):
        if self.results_info is not None:
            self.results_info.print(self.type)

    def get_name(self):
        name = ""
        if self.data_info is not None:
            name = self.data_info.x_label + " - " + self.data_info.y_label + " - " + self.type
        return name