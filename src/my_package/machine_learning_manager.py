# user define imports
from my_package.log_manager import LogManager
from my_package.database_manager import DatabaseManager
from my_package import statistics as statistics
from my_package import visualizer as visualizer
from my_package.machine_learning_components import LinearRegression
from my_package.data_processor import DataProcessor
from my_package.analysis_info import AnalysisInfo, DataInfo, ResultsInfo


class MachineLearningManager:
    def __init__(self):
        return

    @staticmethod
    def get_data(database_manager, data_map_analysis):
        df = database_manager.load()
        if df.empty:
            print('Database is empty!')
            return None
        df_reduced = df[data_map_analysis.keys()]
        return df_reduced, df

    @staticmethod
    def do_analysis(config):
        logger = LogManager.instance()
        logger.log("Parsing city page text!", logger.Logging_Levels["DEBUG"])

        data_map_analysis = {"city": "city", "visitor": "visitor",
                             "population": "population", "museum": "museum",
                             "city_visitor": "city_visitor"}
        database_manager = DatabaseManager.instance()
        loaded_data, original_data = MachineLearningManager.get_data(database_manager, data_map_analysis)
        if loaded_data is None:
            print('Fail to load the data from database!')
        cleaned_df = DataProcessor.data_cleanup(loaded_data)
        cleaned_original_data = DataProcessor.data_cleanup(original_data)

        analysis_list = []
        data_map = {"city": "city",
                    "visitor": "visitor",
                    "population": "population",
                    "city_visitor": "city_visitor",
                    "established":"established",
                    "type":"type",
                    "museum": "museum"}
        DataProcessor.multiple_linear_data(cleaned_original_data, data_map, config)

        data_map = {"city": "city", "visitor": "visitor", "population": "population", "museum": "museum"}
        data_info = DataProcessor.population_visitors(cleaned_df, data_map, config)
        analysis_list.append(AnalysisInfo(data_info=data_info, type="All"))

        data_info = DataProcessor.population_visitors_max(cleaned_df, data_map)
        analysis_list.append(AnalysisInfo(data_info=data_info, type="Max"))

        data_info = DataProcessor.population_visitors_sum(cleaned_df, data_map)
        analysis_list.append(AnalysisInfo(data_info=data_info, type="Sum"))

        data_map = {"city": "city", "visitor": "visitor", "city_visitor": "city_visitor", "museum": "museum"}
        data_info = DataProcessor.city_visitor_museum_visitors(cleaned_df, data_map, config)
        analysis_list.append(AnalysisInfo(data_info=data_info, type="All"))

        data_info = DataProcessor.city_visitor_museum_visitors_max(cleaned_df, data_map)
        analysis_list.append(AnalysisInfo(data_info=data_info, type="Max"))

        data_info = DataProcessor.city_visitor_museum_visitors_sum(cleaned_df, data_map)
        analysis_list.append(AnalysisInfo(data_info=data_info, type="Sum"))

        silent_mode_enabled = config.silent_mode_enabled
        for analysis in analysis_list:
            LinearRegression.perform_analysis(analysis)
            visualizer.plot_results(analysis, silent_mode_enabled)
            visualizer.scatter_plot_results(analysis, silent_mode_enabled)
            if logger.debug_enabled():
                visualizer.print_result(analysis)

        visualizer.scatter_plots(analysis_list, "Linear Regression analysis results", silent_mode_enabled)
        visualizer.print_regression_results(analysis_list, True)
        # visualizer.print_smart_table(analysis_list, " Linear Regression analysis results")