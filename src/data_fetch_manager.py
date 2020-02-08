# user define imports
from src.factory import ParserGenerator as ParserGenerator
import src.wiki_extractor as extractor
import src.util as util
from src.database_manager import DatabaseManager
from src.parser import TableParser
from src.log_manager import LogManager

# python imports
import re

class DataFetchManager:
    def __init__(self):
        return

    @staticmethod
    def fetch_data(config):
        logger = LogManager.instance()
        page_name = config.main_page_name
        parser_list = [ParserGenerator.parser_types['table'], ParserGenerator.parser_types['infobox']]
        parser_instance = ParserGenerator(parser_list)
        # todo: move this to a parser for csv table
        table2 = extractor.make_request_csv()
        tables_txt = table2.splitlines()
        head = ["city", "city_visitor", "city_visitor_reported_year"]
        import pandas as pd
        df_parsed_table_2 = pd.DataFrame(columns=head)
        for i in range(1, len(tables_txt), 1):
            city_info = tables_txt[i]
            delimiter1 = ","
            delimiter2 = '"'
            delimiter3 = ",,"
            test = city_info.split(delimiter3)
            test2 = test[0].split(delimiter2)
            city_name = test2[0]
            city_name = city_name.replace(delimiter1, "")
            city_visitors = test2[1]
            values = test[1].split(delimiter1)
            data = [city_name, city_visitors, values[0]]
            df_parsed_table_2 = df_parsed_table_2.append(pd.Series(data, index=head), ignore_index=True)

        text, _ = extractor.make_request(page_name)
        df_parsed_table = parser_instance.run_function(ParserGenerator.parser_types['table'], text)
        parsed_table = df_parsed_table.values.tolist()
        # todo: group by city so you retrive city page only once
        #      take advantage of panda
        for i in range(1, len(parsed_table), 1):
            city_name = parsed_table[i][1]
            print(city_name)
            text, redirect_page = extractor.make_request(city_name)
            if redirect_page:
                city_name = text.split('[[')[1].split(']]')[0]
                text = extractor.make_request(city_name)[0]

            extracted_city_infos = parser_instance.run_function(ParserGenerator.parser_types['infobox'], text)

            if logger.debug_enabled():
                file_name = city_name + "_info.txt"
                full_path = util.get_full_output_path(file_name)
                if len(extracted_city_infos) > 0:
                    with open(full_path, "w", encoding="utf-8") as file:
                        for key, value in extracted_city_infos.items():
                            file.write(key + ": " + value + "\n")

            museum_name = parsed_table[i][0]
            print(museum_name)

            # I might look at category for "Tokyo Metropolitan Art Museum"
            # there I might have link to real website
            # Category: National Museum of Nature and Science
            if 'Zhejiang Museum' in museum_name or \
                    'Chongqing Museum of Natural History' in museum_name or \
                    "Mevlana Museum" in museum_name or \
                    "Tokyo Metropolitan Art Museum" in museum_name or \
                    "Chengdu Museum" in museum_name or \
                    "Royal Museums Greenwich" in museum_name or \
                    "National Museum of Nature and Science" in museum_name or \
                    "Suzhou Museum" in museum_name or \
                    "Three Gorges Museum" in museum_name or \
                    "Russian Museum" in museum_name:
                # bad website can not extract it is information, missing data case
                # escape it
                continue;

            # invalid case, page does not exist
            if "Reina Sofía" in museum_name or \
                    "National Art Center" in museum_name or \
                    "Museo Nacional de Historia" in museum_name or \
                    "NGV International" in museum_name:
                continue

            text, redirect_page = extractor.make_request(museum_name)
            if redirect_page:
                museum_name = text.split('[[')[1].split(']]')[0]
                text = extractor.make_request(museum_name)[0]

            extracted_museum_infos = parser_instance.run_function(ParserGenerator.parser_types['infobox'], text)
            # Remove all special characters, punctuation and spaces from string
            new_name = re.sub('[^A-Za-z0-9]+', '', museum_name)

            if logger.debug_enabled():
                file_name = new_name + "_info.txt"
                full_path = util.get_full_output_path(file_name)
                if len(extracted_museum_infos) > 0:
                    with open(full_path, "w", encoding="utf-8") as file:
                        for key, value in extracted_museum_infos.items():
                            file.write(key + ": " + value + "\n")
            #  todo: move this to its ovn function to post-process
            # save city and one of its museums in a database
            extracted_city_infos["name"] = parsed_table[i][TableParser.column_type["city"]]
            extracted_museum_infos["name"] = parsed_table[i][TableParser.column_type["museum"]]
            extracted_museum_infos["visitors"] = parsed_table[i][TableParser.column_type["visitor"]]
            extracted_museum_infos["year"] = parsed_table[i][TableParser.column_type["year"]]

            city_visitor_info = df_parsed_table_2[df_parsed_table_2['city'] == extracted_city_infos["name"]]
            if (len(city_visitor_info) > 0):
                extracted_city_infos["city_visitor"] = city_visitor_info["city_visitor"].to_string(index=False)
                extracted_city_infos["city_visitor_reported_year"] = city_visitor_info[
                    "city_visitor_reported_year"].to_string(index=False)

            argument_list = {'city': extracted_city_infos, "museum": extracted_museum_infos}  # percent of original size
            database_manager = DatabaseManager.instance()
            database_manager.save(**argument_list)
