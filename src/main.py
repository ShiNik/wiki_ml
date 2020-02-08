# user define imports
import my_package
from my_package import config
from my_package.log_manager import LogManager
from my_package.database_manager import  DatabaseManager
from my_package import machine_learning_manager as ml
from my_package import data_fetch_manager as data_fetch

# from src.log_manager import LogManager
# from src.database_manager import DatabaseManager
# import src.config as config
# import src.machine_learning_manager as ml
# import src.data_fetch_manager as data_fetch


# step 1: parse the main page : List_of_most_visited_museums
# step 2: generate the table
# stet 3: parse the museum page
# step 4: extract museum information
# step 5: parse the city page
# step 6: extract city information

def print_main_menu():
    print('press d to fetch data: ')
    print('press m for ml: ')
    print('press e for exit: ')


def main():
    logger = LogManager.instance()
    logger.log("Staring the application!", logger.Logging_Levels["DEBUG"])
    database_manager = DatabaseManager.instance()
    database_manager.init(config)

    print_main_menu()
    general_action = input()
    if general_action == 'e':
        return

    if general_action == 'm':
        ml.MachineLearningManager.do_analysis()
        return

    if general_action == 'd':
        database_manager.delete_all_data()
        data_fetch.DataFetchManager.fetch_data(config)
        return


main()
