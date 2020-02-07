#user define imports
from  src.log_manager import LogManager
from src.database_manager import DatabaseManager
import src.config as config
import src.plots as plots

import src.machine_learning_manager as ml
import src.data_fetch_manager as data_fetch

#step 1: parse the main page : List_of_most_visited_museums
#step 2: generate the table
#spet 3: parse the musium page
#step 4: extract musium information
#spet 5: parse the city page
#step 6: extract city information

def print_main_menu():
    print('press d for data fetching: ')
    print('press m for ml: ')
    print('press e for exit: ')

def main():
    logger = LogManager()
    logger.log("Staring the application!", LogManager.Logging_Levels["DEBUG"])
    datbase_manager = DatabaseManager.instance()
    datbase_manager.init(config)

    print_main_menu()
    general_action = input()
    if general_action == 'e':
        return

    if general_action == 'm':
        ml.MachineLearningManager.do_analysis()
        return

    if general_action == 'd':
        datbase_manager.delete_all_data()
        data_fetch.DataFetchManager.fetching_data(config,logger)
        return

main()