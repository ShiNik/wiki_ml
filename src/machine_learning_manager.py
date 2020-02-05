#user define imports
import src.util as util

#python imports
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import re

class Singleton:
    """
    A non-thread-safe helper class to ease implementing singletons.
    This should be used as a decorator -- not a metaclass -- to the
    class that should be a singleton.

    The decorated class can define one `__init__` function that
    takes only the `self` argument. Also, the decorated class cannot be
    inherited from. Other than that, there are no restrictions that apply
    to the decorated class.

    To get the singleton instance, use the `instance` method. Trying
    to use `__call__` will result in a `TypeError` being raised.

    """

    def __init__(self, decorated):
        self._decorated = decorated

    def instance(self):
        """
        Returns the singleton instance. Upon its first call, it creates a
        new instance of the decorated class and calls its `__init__` method.
        On all subsequent calls, the already created instance is returned.

        """
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)

@Singleton
class Foo:
    def __init__(self):
        self.x = 10
        print('Foo created')
    def update(self):
        self.x = self.x + 10

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
    def ml_1():
        file_name = "_most_visited_museums_city_population.csv"
        full_path = util.get_full_output_path(file_name)
        df = pd.read_csv(full_path)
        df_clean = df[['population', 'visitor']]

        data = []
        x_population = []
        y_visitor = []
        for row_info in df_clean.iterrows():
            row = row_info[1]
            if 'c_p' != row["population"] and 'Spain' not in row["population"]:
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

    @staticmethod
    def ml_2():
        file_name = "_most_visited_museums_city_population.csv"
        full_path = util.get_full_output_path(file_name)
        df = pd.read_csv(full_path)
        df_clean = df[['population', 'visitor']]

        data = []
        x_population = []
        y_visitor = []
        for row_info in df_clean.iterrows():
            row = row_info[1]
            if 'c_p' != row["population"] and 'Spain' not in row["population"]:
                population = float(row["population"])
                x_population.append(population)

                key = ","
                visitor = row['visitor']
                if key in visitor:
                    visitor = visitor.replace(",", "")
                visitor = float(visitor)
                y_visitor.append(visitor)

                data.append([population, visitor])


        median = np.median(np.array(x_population))
        mean = np.mean(np.array(x_population))
        max = np.max(np.array(x_population))
        min = np.min(np.array(x_population))
        print(median,mean,max,min)


        x_med_low_p=[]
        x_med_high_p = []
        y_med_low_v = []
        y_med_high_v = []

        x_men_low_p=[]
        x_men_high_p = []
        y_men_low_v = []
        y_men_high_v = []
        for i in range(len(y_visitor)):
            if x_population[i]<median:
                x_med_low_p.append(x_population[i])
                y_med_low_v.append(y_visitor[i])
            else:
                x_med_high_p.append(x_population[i])
                y_med_high_v.append(y_visitor[i])

            if x_population[i] < mean:
                x_men_low_p.append(x_population[i])
                y_men_low_v.append(y_visitor[i])
            else:
                x_men_high_p.append(x_population[i])
                y_men_high_v.append(y_visitor[i])

        MachineLearningManager.scatter_plot(x_men_low_p, y_men_low_v," mean low ")
        MachineLearningManager.scatter_plot(x_men_high_p, y_men_high_v, " mean high ")

        MachineLearningManager.scatter_plot(x_med_low_p, y_med_low_v," med low ")
        MachineLearningManager.scatter_plot(x_med_high_p, y_med_high_v, " med high ")

        MachineLearningManager.linearRegression(x_men_low_p, y_men_low_v, " mean low ")
        MachineLearningManager.linearRegression(x_men_high_p, y_men_high_v, " mean high ")

        MachineLearningManager.linearRegression(x_med_low_p, y_med_low_v, " med low ")
        MachineLearningManager.linearRegression(x_med_high_p, y_med_high_v, " med high ")

    @staticmethod
    def ml_3():
        file_name = "_most_visited_museums_city_population.csv"
        full_path = util.get_full_output_path(file_name)
        df = pd.read_csv(full_path)
        df_cleaned = df.drop(columns=['c_num_museum', 'c_visitor', "m_built", "c_year", "m_type", "m_built",
                                      "museum","city","year","c_size"])

        x_population = []
        x_established = []
        y_visitor = []
        for row_info in df_cleaned.iterrows():
            row = row_info[1]

            # if 'c_p' != row["population"] and 'Spain' not in row["population"] and \
            #         'c_y' != row["c_year"] and  \
            #         'm_e' != row["m_established"] and  \
            #         'm_t' != row["m_type"] and  \
            #         'm_b' != row["m_built"] and \
            #         'c_s' != row["c_size"] :

            if 'c_p' != row["population"] and 'Spain' not in row["population"] and \
                'm_e' != row["m_established"] and "Start" not in row["m_established"] and \
                 "Peking" not in row["m_established"]:

                population = float(row["population"])
                x_population.append(population)

                key = ","
                visitor = row['visitor']
                if key in visitor:
                    visitor = visitor.replace(",", "")
                visitor = float(visitor)
                y_visitor.append(visitor)

                established = row['m_established']
                established = float(established)
                x_established.append(established)


        print("number samples: ", len(x_population))
        x = np.array(x_population)
        y = np.array(y_visitor)
        MachineLearningManager.scatter_plot(x, y, " All population")
        MachineLearningManager.linearRegression(x, y, " All population")


        x = np.array(x_established)
        y = np.array(y_visitor)
        MachineLearningManager.scatter_plot(x, y, " All established")
        MachineLearningManager.linearRegression(x, y, " All established")

    @staticmethod
    def population_visitors(df, data_map):
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

            print("==============================")
            index = index + 1
            for data in city_info.iterrows():
                str_population = data[1]['population']
                if str_population:
                    print("City name: ",data[1]['city'], "Population:: ", data[1]['population'], "museum: ", data[1]['museum'], "Visitors: ", data[1]['visitor'])
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

           #not sure how
            key = "size"
            if key in heads:
                size = cleaned_df.loc[i, key]
                cleaned_df.loc[i, key] = size

        return cleaned_df

    @staticmethod
    def do_analysis(datbase_manager):
        loaded_data = MachineLearningManager.get_data(datbase_manager)
        cleaned_df =  MachineLearningManager.data_cleanup(loaded_data)
        data_map = {"city":"city", "visitor":"visitor", "population":"population", "museum":"population"}
        MachineLearningManager.population_visitors(cleaned_df, data_map)
        return True