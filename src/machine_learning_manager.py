#user define imports
import src.util as util
from src.database_manager import DatabaseManager
import src.statistics as statistics
import src.plots as plots

#python imports
import numpy as np
import re

class DataInfo:
    def __init__(self, x_data_info, y_data_info):
        self.x_values = x_data_info["values"]
        self.x_label = x_data_info["label"]
        self.y_values = y_data_info["values"]
        self.y_label = y_data_info["label"]

class ResultsInfo:
    def __init__(self):
        self.intercept = None
        self.coef = None
        self.covariance_matrix = None
        self.Pearson_correlation_coefficient = None
        self.spearman_correlation = None

    def print(self, type):
        print("intercept: ",self.intercept,", coef: ", self.coef)
        print(self.covariance_matrix)
        print("Pearson_correlation_coefficient: ", self.Pearson_correlation_coefficient)
        print("spearman_correlation: ", self.spearman_correlation)

class AnalysisInfo:
    def __init__(self, data_info, type):
        self.data_info =  data_info
        self.results_info = None
        self.type = type

    def print(self):
        if self.results_info is not None :
            self.results_info.print(self.type)

    def get_name(self):
        name =  ""
        if self.data_info is not None:
             name = self.data_info.x_label + " - " + self.data_info.y_label + " - " + self.type
        return name

class MachineLearningManager:
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

    @staticmethod
    def population_visitors(df, data_map):
        df_clean = df[['population', 'visitor']]
        x_population = []
        y_visitor = []
        for row_info in df_clean.iterrows():
            row = row_info[1]
            str_population = row["population"]
            if str_population:
                population = float(row["population"])
                x_population.append(population)
                key = ","
                visitor = row['visitor']
                if key in visitor:
                    visitor = visitor.replace(",", "")
                visitor = float(visitor)
                y_visitor.append(visitor)

        x_data_info = {"values":x_population,"label":"City Population"}
        y_data_info = {"values": y_visitor, "label": "Museum Visitors"}
        return DataInfo(x_data_info=x_data_info, y_data_info=y_data_info)

    @staticmethod
    def population_visitors_sum(df, data_map):
        df_clean = df[data_map.keys()]
        grouped_df = df_clean.groupby(["city"])
        number_cities = grouped_df.ngroups
        print("number of cities: " , number_cities)

        number_features = 2
        index = -1
        train_id_info = np.zeros((number_cities, number_features), dtype=int)
        for city_data in grouped_df:
            city_info = city_data[1]
            index = index + 1
            for data in city_info.iterrows():
                str_population = data[1]['population']
                if str_population:
                    col = 0
                    population = float(data[1]['population'])
                    train_id_info[index,col] = population

                    col = col + 1
                    visitor = float(data[1]['visitor'])
                    train_id_info[index, col] = train_id_info[index, col] + visitor
        x_population = []
        y_visitor = []
        for data in train_id_info:
            if data[0] != 0:
                #population
                x_population.append(data[0])
                #visitor
                y_visitor.append(data[1])

        x_data_info = {"values": x_population, "label": "City Population"}
        y_data_info = {"values": y_visitor, "label": "Museum Visitors"}
        return DataInfo(x_data_info=x_data_info, y_data_info=y_data_info)

    @staticmethod
    def population_visitors_max(df, data_map):
        df_clean = df[data_map.keys()]
        grouped_df = df_clean.groupby(["city"])
        number_cities = grouped_df.ngroups
        print("number of cities: " , number_cities)

        number_features = 2
        index = -1
        train_id_info = np.zeros((number_cities, number_features), dtype=int)
        for city_data in grouped_df:
            city_info = city_data[1]
            index = index + 1
            for data in city_info.iterrows():
                str_population = data[1]['population']
                if str_population:
                    col = 0
                    population = float(data[1]['population'])
                    train_id_info[index,col] = population

                    col = col + 1
                    visitor = float(data[1]['visitor'])

                    train_id_info[index, col] = max(train_id_info[index, col], visitor)

        x_population = []
        y_visitor = []
        for data in train_id_info:
            if data[0] != 0:
                #population
                x_population.append(data[0])
                #visitor
                y_visitor.append(data[1])

        x_data_info = {"values": x_population, "label": "City Population"}
        y_data_info = {"values": y_visitor, "label": "Museum Visitors"}
        return DataInfo(x_data_info=x_data_info, y_data_info=y_data_info)

    @staticmethod
    def city_visitor_museum_visitors(df, data_map):
        df_clean = df[['city_visitor', 'visitor']]
        x_city_visitor = []
        y_visitor = []

        for row_info in df_clean.iterrows():
            row = row_info[1]
            str_city_visitor = row["city_visitor"]
            if str_city_visitor:
                city_visitor = float(row["city_visitor"])
                x_city_visitor.append(city_visitor)

                key = ","
                visitor = row['visitor']
                if key in visitor:
                    visitor = visitor.replace(",", "")
                visitor = float(visitor)
                y_visitor.append(visitor)

        x_data_info = {"values": x_city_visitor, "label": "City Visitors"}
        y_data_info = {"values": y_visitor, "label": "Museum Visitors"}
        return DataInfo(x_data_info=x_data_info, y_data_info=y_data_info)

    @staticmethod
    def city_visitor_museum_visitors_sum(df, data_map):
        df_clean = df[data_map.keys()]
        grouped_df = df_clean.groupby(["city"])
        number_cities = grouped_df.ngroups
        print("number of cities: " , number_cities)

        number_features = 2
        index = -1
        train_id_info = np.zeros((number_cities, number_features), dtype=int)
        for city_data in grouped_df:
            train_id_label_info = 0

            city_info = city_data[1]

            total_visitors = 0

            index = index + 1
            for data in city_info.iterrows():
                str_city_visitor = data[1]['city_visitor']
                if str_city_visitor:
                    col = 0
                    city_visitor = float(data[1]['city_visitor'])
                    train_id_info[index,col] = city_visitor

                    col = col + 1
                    visitor = float(data[1]['visitor'])
                    train_id_info[index, col] = train_id_info[index, col] + visitor

        x_city_visitor = []
        y_visitor = []
        for data in train_id_info:
            if data[0] != 0:
                #population
                x_city_visitor.append(data[0])
                #visitor
                y_visitor.append(data[1])

        x_data_info = {"values": x_city_visitor, "label": "City Visitors"}
        y_data_info = {"values": y_visitor, "label": "Museum Visitors"}
        return DataInfo(x_data_info=x_data_info, y_data_info=y_data_info)

    @staticmethod
    def city_visitor_museum_visitors_max(df, data_map):
        df_clean = df[data_map.keys()]
        grouped_df = df_clean.groupby(["city"])
        number_cities = grouped_df.ngroups
        print("number of cities: " , number_cities)

        number_features = 2
        index = -1
        train_id_info = np.zeros((number_cities, number_features), dtype=int)
        for city_data in grouped_df:
            city_info = city_data[1]
            index = index + 1
            for data in city_info.iterrows():
                str_city_visitor = data[1]['city_visitor']
                if str_city_visitor:
                    col = 0
                    city_visitor = float(data[1]['city_visitor'])
                    train_id_info[index,col] = city_visitor

                    col = col + 1
                    visitor = float(data[1]['visitor'])

                    train_id_info[index, col] = max(train_id_info[index, col], visitor)

        x_city_visitor = []
        y_visitor = []
        for data in train_id_info:
            if data[0] != 0:
                #population
                x_city_visitor.append(data[0])
                #visitor
                y_visitor.append(data[1])

        x_data_info = {"values": x_city_visitor, "label": "City Visitors"}
        y_data_info = {"values": y_visitor, "label": "Museum Visitors"}
        return DataInfo(x_data_info=x_data_info, y_data_info=y_data_info)

    @staticmethod
    def get_data(datbase_manager, data_map_analysis):
        df =  datbase_manager.load()
        df_reduced = df[data_map_analysis.keys()]
        return df_reduced


    @staticmethod
    def clean_year(str_year):
        p = re.compile('(\d{4})')
        result_re = p.findall(str_year)
        return  "" if len(result_re) == 0 else result_re[0]

    @staticmethod
    def clean_number(str_number):
        a = '\b(\d*,\d*)\b'
        b = '[^0-9]+'
        result_re = re.sub(b, '', str_number)
        return '' if len(result_re) == 0 else result_re

    @staticmethod
    def data_cleanup(df):
        cleaned_df = df
        heads = {i:df.columns.get_loc(i) for i in df.columns}
        for i in range(len(df)):
            key ="population"
            if key in heads:
                population = cleaned_df.loc[i, key]
                cleaned_df.loc[i, key] = "" if not population else MachineLearningManager.clean_number(population)

            key ="visitor"
            if key in heads:
                visitor = cleaned_df.loc[i, key]
                cleaned_df.loc[i, key] = "" if not visitor else MachineLearningManager.clean_number(visitor)

            key ="year_reported"
            if key in heads:
                year = cleaned_df.loc[i, key]
                cleaned_df.loc[i, key] = "" if not year else MachineLearningManager.clean_year(year)

            key ="established"
            if key in heads:
                year = cleaned_df.loc[i, key]
                cleaned_df.loc[i, key] = "" if not year else MachineLearningManager.clean_year(year)

            key ="built"
            if key in heads:
                year = cleaned_df.loc[i, key]
                cleaned_df.loc[i, key] = "" if not year else MachineLearningManager.clean_year(year)

            key ="city_visitor"
            if key in heads:
                visitor = cleaned_df.loc[i, key]
                cleaned_df.loc[i, key] = "" if not visitor else MachineLearningManager.clean_number(visitor)

           #not sure how
            key = "size"
            if key in heads:
                size = cleaned_df.loc[i, key]
                cleaned_df.loc[i, key] = size

        return cleaned_df

    @staticmethod
    def do_analysis():
        data_map_analysis = {"city":"city", "visitor":"visitor",
                             "population":"population", "museum":"museum",
                             "city_visitor":"city_visitor"}
        datbase_manager = DatabaseManager.instance()
        loaded_data = MachineLearningManager.get_data(datbase_manager, data_map_analysis)
        cleaned_df =  MachineLearningManager.data_cleanup(loaded_data)
        analysis_list = []
        data_map = {"city":"city", "visitor":"visitor", "population":"population", "museum":"museum"}
        data_info = MachineLearningManager.population_visitors(cleaned_df, data_map)
        analysis_list.append(AnalysisInfo(data_info=data_info,type="All"))

        data_info = MachineLearningManager.population_visitors_max(cleaned_df, data_map)
        analysis_list.append(AnalysisInfo(data_info=data_info, type="Max"))

        data_info = MachineLearningManager.population_visitors_sum(cleaned_df, data_map)
        analysis_list.append(AnalysisInfo(data_info=data_info, type="Sum"))

        data_map = {"city": "city", "visitor": "visitor", "city_visitor": "city_visitor", "museum": "museum"}
        data_info = MachineLearningManager.city_visitor_museum_visitors(cleaned_df, data_map)
        analysis_list.append(AnalysisInfo(data_info=data_info, type="All"))

        data_info = MachineLearningManager.city_visitor_museum_visitors_max(cleaned_df, data_map)
        analysis_list.append(AnalysisInfo(data_info=data_info, type="Max"))

        data_info = MachineLearningManager.city_visitor_museum_visitors_sum(cleaned_df, data_map)
        analysis_list.append(AnalysisInfo(data_info=data_info, type="Sum"))

        for analysis in analysis_list:
            x_t = analysis.data_info.x_label
            y_t = analysis.data_info.y_label
            type = analysis.type
            print("============= " + analysis.get_name() + " ===============")
            MachineLearningManager.perform_analysis(analysis)
            analysis.print()

        plots.scatter_plots(analysis_list, " Linear Regression analysis reesults")
