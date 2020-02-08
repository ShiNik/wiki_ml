# user define imports
from my_package import util as util
from my_package.analysis_info import AnalysisInfo, DataInfo, ResultsInfo
from my_package.data_cleaner import DataCleaner

# python imports
import numpy as np


class DataProcessor:
    def __init__(self):
        return

    @staticmethod
    def data_cleanup(df):
        return DataCleaner.perform_cleanup(df)

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

        x_data_info = {"values": x_population, "label": "City Population"}
        y_data_info = {"values": y_visitor, "label": "Museum Visitors"}
        return DataInfo(x_data_info=x_data_info, y_data_info=y_data_info)

    @staticmethod
    def population_visitors_sum(df, data_map):
        df_clean = df[data_map.keys()]
        grouped_df = df_clean.groupby(["city"])
        number_cities = grouped_df.ngroups
        print("number of cities: ", number_cities)

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
                    train_id_info[index, col] = population

                    col = col + 1
                    visitor = float(data[1]['visitor'])
                    train_id_info[index, col] = train_id_info[index, col] + visitor
        x_population = []
        y_visitor = []
        for data in train_id_info:
            if data[0] != 0:
                # population
                x_population.append(data[0])
                # visitor
                y_visitor.append(data[1])

        x_data_info = {"values": x_population, "label": "City Population"}
        y_data_info = {"values": y_visitor, "label": "Museum Visitors"}
        return DataInfo(x_data_info=x_data_info, y_data_info=y_data_info)

    @staticmethod
    def population_visitors_max(df, data_map):
        df_clean = df[data_map.keys()]
        grouped_df = df_clean.groupby(["city"])
        number_cities = grouped_df.ngroups
        print("number of cities: ", number_cities)

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
                    train_id_info[index, col] = population

                    col = col + 1
                    visitor = float(data[1]['visitor'])

                    train_id_info[index, col] = max(train_id_info[index, col], visitor)

        x_population = []
        y_visitor = []
        for data in train_id_info:
            if data[0] != 0:
                # population
                x_population.append(data[0])
                # visitor
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
        print("number of cities: ", number_cities)

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
                    train_id_info[index, col] = city_visitor

                    col = col + 1
                    visitor = float(data[1]['visitor'])
                    train_id_info[index, col] = train_id_info[index, col] + visitor

        x_city_visitor = []
        y_visitor = []
        for data in train_id_info:
            if data[0] != 0:
                # population
                x_city_visitor.append(data[0])
                # visitor
                y_visitor.append(data[1])

        x_data_info = {"values": x_city_visitor, "label": "City Visitors"}
        y_data_info = {"values": y_visitor, "label": "Museum Visitors"}
        return DataInfo(x_data_info=x_data_info, y_data_info=y_data_info)

    @staticmethod
    def city_visitor_museum_visitors_max(df, data_map):
        df_clean = df[data_map.keys()]
        grouped_df = df_clean.groupby(["city"])
        number_cities = grouped_df.ngroups
        print("number of cities: ", number_cities)

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
                    train_id_info[index, col] = city_visitor

                    col = col + 1
                    visitor = float(data[1]['visitor'])

                    train_id_info[index, col] = max(train_id_info[index, col], visitor)

        x_city_visitor = []
        y_visitor = []
        for data in train_id_info:
            if data[0] != 0:
                # population
                x_city_visitor.append(data[0])
                # visitor
                y_visitor.append(data[1])

        x_data_info = {"values": x_city_visitor, "label": "City Visitors"}
        y_data_info = {"values": y_visitor, "label": "Museum Visitors"}
        return DataInfo(x_data_info=x_data_info, y_data_info=y_data_info)
