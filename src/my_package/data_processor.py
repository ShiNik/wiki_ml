# user define imports
from my_package.analysis_info import AnalysisInfo, DataInfo, ResultsInfo
from my_package.data_cleaner import DataCleaner
from my_package import visualizer as visualizer

# python imports
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


class DataProcessor:
    def __init__(self):
        return

    @staticmethod
    def data_cleanup(df):
        return DataCleaner.perform_cleanup(df)

    @staticmethod
    def train_test_split(dataset, x_name, y_name, test_size):
        X = dataset[x_name].values.reshape(-1, 1)
        y = dataset[y_name].values.reshape(-1, 1)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
        return X_train, X_test, y_train, y_test

    @staticmethod
    def population_visitors(df, data_map, config):

        df_selected = df[['population', 'visitor']]
        df_selected.loc[:, 'population'] = pd.to_numeric(df_selected.loc[:, 'population'])
        df_selected.loc[:, 'visitor'] = pd.to_numeric(df_selected.loc[:, 'visitor'])
        df_clean = df_selected.dropna()

        file_name = "distribution_All_MuseumVisitors_Function_population_visitors.png"
        silent_mode_enabled = config.silent_mode_enabled
        visualizer.plot_data_distribution(df_clean['visitor'], file_name, silent_mode_enabled)

        file_name = "distribution_All_CityPopulation_Function_population_visitors.png"
        silent_mode_enabled = config.silent_mode_enabled
        visualizer.plot_data_distribution(df_clean['population'], file_name, silent_mode_enabled)

        labels = {"x": ["population", "City Population"], "y": ["visitor", "Museum Visitors"]}
        visualizer.plot_data(df_clean, labels, silent_mode_enabled)

        x_population = df_clean['population'].to_numpy()
        y_visitor = df_clean['visitor'].to_numpy()

        visualizer.quantile_quantile_plot(y_visitor, silent_mode_enabled)
        visualizer.quantile_quantile_plot(x_population, silent_mode_enabled)

        X_train, X_test, y_train, y_test = DataProcessor.train_test_split(df_clean, "population", "visitor", 0.2)
        x_data_info = {"values": x_population.tolist(), "label": "City Population", "train":X_train, "test":X_test}
        y_data_info = {"values": y_visitor.tolist(), "label": "Museum Visitors", "train":y_train, "test":y_test}
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
    def city_visitor_museum_visitors(df, data_map, config):

        df_selected = df[['city_visitor', 'visitor']]
        df_selected.loc[:, 'city_visitor'] = pd.to_numeric(df_selected.loc[:, 'city_visitor'])
        df_selected.loc[:, 'visitor'] = pd.to_numeric(df_selected.loc[:, 'visitor'])
        df_clean = df_selected.dropna()

        file_name = "distribution_All_MuseumVisitors_Function_city_visitor_museum_visitors.png"
        silent_mode_enabled = config.silent_mode_enabled
        visualizer.plot_data_distribution(df_clean['visitor'], file_name, silent_mode_enabled)

        file_name = "distribution_All_CityVisitors_Function_city_visitor_museum_visitors.png"
        silent_mode_enabled = config.silent_mode_enabled
        visualizer.plot_data_distribution(df_clean['city_visitor'], file_name, silent_mode_enabled)

        labels = {"x": ["city_visitor", "City Visitors"], "y": ["visitor", "Museum Visitors"]}
        visualizer.plot_data(df_clean, labels, silent_mode_enabled)

        x_city_visitor = df_clean['city_visitor'].to_numpy()
        y_visitor = df_clean['visitor'].to_numpy()

        X_train, X_test, y_train, y_test = DataProcessor.train_test_split(df_clean, "city_visitor", "visitor", 0.2)

        x_data_info = {"values": x_city_visitor.tolist(), "label": "City Visitors", "train":X_train, "test":X_test}
        y_data_info = {"values": y_visitor.tolist(), "label": "Museum Visitors", "train":y_train, "test":y_test}
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


    @staticmethod
    def multiple_linear_data(dataset, data_map, config):
        #todo: this function should be refactor,
        # new machine _learning_component is needed

        dataset = dataset[data_map.keys()]
        dataset.loc[:, 'population'] = pd.to_numeric(dataset.loc[:, 'population'])
        dataset.loc[:, 'visitor'] = pd.to_numeric(dataset.loc[:, 'visitor'])
        dataset.loc[:, 'established'] = pd.to_numeric(dataset.loc[:, 'established'])
        dataset.loc[:, 'city_visitor'] = pd.to_numeric(dataset.loc[:, 'city_visitor'])

        dataset = dataset.dropna()
        museum_types = dataset["type"].unique()
        museum_id = 0
        for type in museum_types:
            if type:
                museum_id = museum_id + 1
                dataset.loc[dataset["type"] == type, "type"] = museum_id
            else:
                dataset.loc[dataset["type"] == type, "type"] = -1

        dataset= dataset[dataset["type"] != -1]

        X = dataset[['population', 'established', 'city_visitor', 'type']].values
        y = dataset['visitor'].values

        file_name = "distribution_All_MuseumVisitors_Function_multiple_linear_data.png"
        silent_mode_enabled = config.silent_mode_enabled
        visualizer.plot_data_distribution(dataset['visitor'], file_name, silent_mode_enabled)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

        x_data_info = {"values": None, "label": "multiple_linear", "train": X_train, "test": X_test}
        y_data_info = {"values": None, "label": "Museum Visitors", "train": y_train, "test": y_test}
        data_info = DataInfo(x_data_info=x_data_info, y_data_info=y_data_info)
        analysis = AnalysisInfo(data_info=data_info, type="All")

        from sklearn.linear_model import LinearRegression
        from sklearn import metrics

        regressor = LinearRegression()
        regressor.fit(X_train, y_train)  # training the algorithm
        y_pred = regressor.predict(X_test)
        df = pd.DataFrame({'Actual': y_test.flatten(), 'Predicted': y_pred.flatten()})

        analysis.results_info = ResultsInfo()
        analysis.results_info.prediction = y_pred
        analysis.results_info.y_test = y_test

        visualizer.plot_results(analysis, silent_mode_enabled)

        print("========== Multiple linear regression =================")
        print(df)
        # For retrieving the slope:
        print('coefficient',"\n")
        print("population: ", regressor.coef_[0])
        print("established: ", regressor.coef_[1])
        print("city_visitor: ", regressor.coef_[2])
        print("type: ", regressor.coef_[3])
        print('Intercept:', regressor.intercept_)
        print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))
        print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))
        print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))
