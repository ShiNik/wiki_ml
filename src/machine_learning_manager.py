# user define imports
import src.util as util
from src.log_manager import LogManager
from src.database_manager import DatabaseManager
import src.statistics as statistics
import src.visualizer as visualizer
from src.machine_learning_components import LinearRegression
from src.data_processor import DataProcessor
from src.analysis_info import AnalysisInfo, DataInfo, ResultsInfo


# python imports

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
        return df_reduced

    @staticmethod
    def do_analysis():
        logger = LogManager.instance()
        logger.log("Parsing city page text!", logger.Logging_Levels["DEBUG"])

        data_map_analysis = {"city": "city", "visitor": "visitor",
                             "population": "population", "museum": "museum",
                             "city_visitor": "city_visitor"}
        database_manager = DatabaseManager.instance()
        loaded_data = MachineLearningManager.get_data(database_manager, data_map_analysis)
        if loaded_data is None:
            print('Fail to load the data from database!')
        cleaned_df = DataProcessor.data_cleanup(loaded_data)

        analysis_list = []
        data_map = {"city": "city", "visitor": "visitor", "population": "population", "museum": "museum"}
        data_info = DataProcessor.population_visitors(cleaned_df, data_map)
        analysis_list.append(AnalysisInfo(data_info=data_info, type="All"))

        data_info = DataProcessor.population_visitors_max(cleaned_df, data_map)
        analysis_list.append(AnalysisInfo(data_info=data_info, type="Max"))

        data_info = DataProcessor.population_visitors_sum(cleaned_df, data_map)
        analysis_list.append(AnalysisInfo(data_info=data_info, type="Sum"))

        data_map = {"city": "city", "visitor": "visitor", "city_visitor": "city_visitor", "museum": "museum"}
        data_info = DataProcessor.city_visitor_museum_visitors(cleaned_df, data_map)
        analysis_list.append(AnalysisInfo(data_info=data_info, type="All"))

        data_info = DataProcessor.city_visitor_museum_visitors_max(cleaned_df, data_map)
        analysis_list.append(AnalysisInfo(data_info=data_info, type="Max"))

        data_info = DataProcessor.city_visitor_museum_visitors_sum(cleaned_df, data_map)
        analysis_list.append(AnalysisInfo(data_info=data_info, type="Sum"))

        for analysis in analysis_list:
            LinearRegression.perform_analysis(analysis)
            visualizer.print_result(analysis)

        visualizer.scatter_plots(analysis_list, " Linear Regression analysis results")
