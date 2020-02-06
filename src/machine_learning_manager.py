#user define imports
import src.util as util
from src.database_manager import DatabaseManager

#python imports
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import re

class MachineLearningManager:
    def __init__(self):
        return

    @staticmethod
    def scatter_plot(x,y,test_id):
        import matplotlib.pyplot as plt
        fig=plt.figure()
        ax=fig.add_axes([0,0,1,1])
        ax.scatter(x, y, color='r')
        ax.set_xlabel('population ' + test_id)
        ax.set_ylabel('visitor ' + test_id)
        ax.set_title('scatter plot')
        xx = np.zeros(2)
        xx[0]= np.min(x)
        xx[1] = np.max(x)
        yy = xx+10
        plt.plot(xx,yy, linestyle = "solid")
        plt.show()

    @staticmethod
    def correlation_coef(x,y):
        np.corrcoef()

    @staticmethod
    def covariance(x,y):

        # calculate the covariance between two variables
        from numpy.random import randn
        from numpy.random import seed
        from numpy import cov

        # calculate covariance matrix
        covariance = cov(x, y)
        print(covariance)

    @staticmethod
    def Pearson_correlation_coefficient(x,y):
        # calculate the Pearson's correlation between two variables
        from numpy.random import randn
        from numpy.random import seed
        from scipy.stats import pearsonr
        # calculate Pearson's correlation
        corr, _ = pearsonr(x, y)
        print('Pearsons correlation: %.3f' % corr)

    @staticmethod
    def spearman_correlation(x,y):
        # calculate the spearmans's correlation between two variables
        from numpy.random import randn
        from numpy.random import seed
        from scipy.stats import spearmanr
        # seed random number generator

        # calculate spearman's correlation
        corr, _ = spearmanr(x, y)
        print('Spearmans correlation: %.3f' % corr)


    @staticmethod
    def linearRegression(x,y,test_id):
        X = np.array(x).reshape(-1, 1)
        y = np.array(y).reshape(-1, 1)
        reg = LinearRegression().fit(X, y)
        print("=================")
        print(test_id)
        print("score: ", reg.score(X, y))
        print("intercept: ", reg.intercept_)
        print("coef: ", reg.coef_)

    @staticmethod
    def population_visitors(df, data_map):
        df_clean = df[['population', 'visitor']]

        data = []
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

                data.append([population, visitor])

        x = np.array(x_population)
        y = np.array(y_visitor)
        MachineLearningManager.scatter_plot(x, y, " All ")
        MachineLearningManager.linearRegression(x, y, " All ")

        # find the relationship
        MachineLearningManager.covariance(x, y)

        # to find strength we use pearson correlation coefficient
        MachineLearningManager.Pearson_correlation_coefficient(x, y)

        # Two  variables may be related by a nonlinear relationship
        MachineLearningManager.spearman_correlation(x, y)

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
            train_id_label_info = 0

            city_info = city_data[1]

            total_visitors = 0

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


        x = np.array(x_population)
        y = np.array(y_visitor)
        MachineLearningManager.scatter_plot(x, y, "All population and  visitor")
        MachineLearningManager.linearRegression(x, y, " All population and  visitor ")

        # find the relationship
        MachineLearningManager.covariance(x, y)

        # to find strength we use pearson correlation coefficient
        MachineLearningManager.Pearson_correlation_coefficient(x,y)

        #Two  variables may be related by a nonlinear relationship
        MachineLearningManager.spearman_correlation(x, y)

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
            train_id_label_info = 0

            city_info = city_data[1]

            total_visitors = 0

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


        x = np.array(x_population)
        y = np.array(y_visitor)
        MachineLearningManager.scatter_plot(x, y, "All population and  visitor")
        MachineLearningManager.linearRegression(x, y, " All population and  visitor ")

        # find the relationship
        MachineLearningManager.covariance(x, y)

        # to find strength we use pearson correlation coefficient
        MachineLearningManager.Pearson_correlation_coefficient(x,y)

        #Two  variables may be related by a nonlinear relationship
        MachineLearningManager.spearman_correlation(x, y)

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

        x = np.array(x_city_visitor)
        y = np.array(y_visitor)
        MachineLearningManager.scatter_plot(x, y, " All ")
        MachineLearningManager.linearRegression(x, y, " All ")

        # find the relationship
        MachineLearningManager.covariance(x, y)

        # to find strength we use pearson correlation coefficient
        MachineLearningManager.Pearson_correlation_coefficient(x, y)

        # Two  variables may be related by a nonlinear relationship
        MachineLearningManager.spearman_correlation(x, y)

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


        x = np.array(x_city_visitor)
        y = np.array(y_visitor)
        MachineLearningManager.scatter_plot(x, y, "All population and  visitor")
        MachineLearningManager.linearRegression(x, y, " All population and  visitor ")

        # find the relationship
        MachineLearningManager.covariance(x, y)

        # to find strength we use pearson correlation coefficient
        MachineLearningManager.Pearson_correlation_coefficient(x,y)

        #Two  variables may be related by a nonlinear relationship
        MachineLearningManager.spearman_correlation(x, y)

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

                    train_id_info[index, col] = max(train_id_info[index, col], visitor)

        x_city_visitor = []
        y_visitor = []
        for data in train_id_info:
            if data[0] != 0:
                #population
                x_city_visitor.append(data[0])
                #visitor
                y_visitor.append(data[1])


        x = np.array(x_city_visitor)
        y = np.array(y_visitor)
        MachineLearningManager.scatter_plot(x, y, "All population and  visitor")
        MachineLearningManager.linearRegression(x, y, " All population and  visitor ")

        # find the relationship
        MachineLearningManager.covariance(x, y)

        # to find strength we use pearson correlation coefficient
        MachineLearningManager.Pearson_correlation_coefficient(x,y)

        #Two  variables may be related by a nonlinear relationship
        MachineLearningManager.spearman_correlation(x, y)

    @staticmethod
    def group_analysis(df, data_map):
        df_clean = df[data_map.keys()]
        grouped_df = df_clean.groupby(["city"])
        number_cities = grouped_df.ngroups
        print("number of cities: " , number_cities)

        number_features = 4
        index = -1
        train_id_info = np.zeros((number_cities, number_features), dtype=int)
        for city_data in grouped_df:
            train_id_label_info = 0

            city_info = city_data[1]

            total_visitors = 0

            index = index + 1
            for data in city_info.iterrows():
                str_city_visitor = data[1]['city_visitor']
                str_population = data[1]['population']
                str_established= data[1]['established']
                if str_city_visitor and str_population and str_established:
                    col = 0
                    city_visitor = float(data[1]['city_visitor'])
                    train_id_info[index,col] = city_visitor

                    col = col + 1
                    population = float(data[1]['population'])
                    train_id_info[index, col] = max(train_id_info[index, col], population)

                    col = col + 1
                    visitor = float(data[1]['visitor'])
                    if train_id_info[index, col]> visitor:
                        train_id_info[index, col] = max(train_id_info[index, col], visitor)

                        col = col + 1
                        established = float(data[1]['established'])
                        train_id_info[index, col] = max(train_id_info[index, col], established)


        x_city_visitor = []
        y_visitor = []
        for data in train_id_info:
            if data[0] != 0:
                #0,1,3
                x_city_visitor.append(data[0])
                x_city_visitor.append(data[1])
                x_city_visitor.append(data[3])
                # 2 visitor
                y_visitor.append(data[2])


        x = np.array(x_city_visitor)
        y = np.array(y_visitor)
        MachineLearningManager.scatter_plot(x, y, "All population and  visitor")
        MachineLearningManager.linearRegression(x, y, " All population and  visitor ")

        # find the relationship
        MachineLearningManager.covariance(x, y)

        # to find strength we use pearson correlation coefficient
        MachineLearningManager.Pearson_correlation_coefficient(x,y)

        #Two  variables may be related by a nonlinear relationship
        MachineLearningManager.spearman_correlation(x, y)


    @staticmethod
    def get_data(datbase_manager):
        # wiki_to_database_city_map = {"name": "name", "population_total": "population",
        #                              "area_total_km2": "size", "population_as_of": "year_reported"}
        #
        # wiki_to_database_museum_map = {"name": "name", "visitor": "visitor", "year": "year_reported",
        #                                "type": "type", "publictransit": "public_transit",
        #                                "location": "location", "established": "established",
        #                                "built": "built"}
        #
        # data_map = {"city", "visitor", "population", "museum" }

        return datbase_manager.load()

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
        datbase_manager = DatabaseManager.instance()
        loaded_data = MachineLearningManager.get_data(datbase_manager)
        cleaned_df =  MachineLearningManager.data_cleanup(loaded_data)
        data_map = {"city":"city", "visitor":"visitor", "population":"population", "museum":"museum"}
        print("===========  population_visitors ===============")
        MachineLearningManager.population_visitors(cleaned_df, data_map)
        print("============= population_visitors_max ===============")
        MachineLearningManager.population_visitors_max(cleaned_df, data_map)
        print("============= population_visitors_sum ===============")
        MachineLearningManager.population_visitors_sum(cleaned_df, data_map)

        data_map = {"city": "city", "visitor": "visitor", "city_visitor": "city_visitor", "museum": "museum"}
        print("===========  city_visitors ===============")
        MachineLearningManager.city_visitor_museum_visitors(cleaned_df, data_map)
        print("============= city_visitors_max ===============")
        MachineLearningManager.city_visitor_museum_visitors_max(cleaned_df, data_map)
        print("============= city_visitors_sum ===============")
        MachineLearningManager.city_visitor_museum_visitors_sum(cleaned_df, data_map)

        data_map = {"city": "city", "visitor": "visitor", "population": "population",
                    "museum": "museum", "city_visitor": "city_visitor",
                    "established":"established"}
        MachineLearningManager.group_analysis(cleaned_df, data_map)

        return True