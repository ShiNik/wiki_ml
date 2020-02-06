#user define imports
from src.factory import ParserGenerator as ParserGenerator
import src.wiki_extractor as extractor
import src.util as util
from src.database_manager import DatabaseManager
from  src.parser import TableParser

class DataFetchManager:
    def __init__(self):
        return

    @staticmethod
    def fetching_data(config, logger):
        page_name = config.main_page_name
        parser_list = [ParserGenerator.parser_types['table'], ParserGenerator.parser_types['infobox']]
        Parser_instance = ParserGenerator(parser_list)

        table2 = extractor.USE_REQUEST_csv()
        tables_txt = table2.splitlines()
        # head = tables_txt[0].split(",")
        head = ["city","city_visitor","city_visitor_reported_year"]
        import pandas as pd
        df_parsed_table_2 = pd.DataFrame(columns=head)
        for i in range(1,len(tables_txt),1):
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
            data = [city_name,city_visitors,values[0]]
            # for value in values:
            #     data.append(value)
            df_parsed_table_2 = df_parsed_table_2.append(pd.Series(data, index = head), ignore_index=True)

        text , _= extractor.USE_REQUEST(page_name)
        df_parsed_table = Parser_instance.run_function(ParserGenerator.parser_types['table'],text, logger)
        parsed_table = df_parsed_table.values.tolist()
        #todo: group by city so you retrive city page only once
        #      take advantage of panda
        for i in range(1, len(parsed_table), 1):
            city_name = parsed_table[i][1]
            print(city_name)
            text, redirect_page = extractor.USE_REQUEST(city_name, True)
            if redirect_page:
                city_name = text.split('[[')[1].split(']]')[0]
                text = extractor.USE_REQUEST(city_name, True)[0]

            if 'Mexico City' in city_name:
                print("shima")
            extracted_city_infos = Parser_instance.run_function(ParserGenerator.parser_types['infobox'],text,logger)

            file_name = city_name + "_info.txt"
            full_path = util.get_full_output_path(file_name)
            if len(extracted_city_infos) > 0:
                with open(full_path , "w", encoding="utf-8") as file:
                    for key, value in extracted_city_infos.items():
                        file.write(key + ": " + value + "\n")

            museum_name = parsed_table[i][0]
            print(museum_name)

            if "Natural History Museum" in museum_name:
                print("shima")

            #I might look at categor for "Tokyo Metropolitan Art Museum"
            #there I might have link to real website
            # Category: National Museum of Nature and Science
            if 'Zhejiang Museum' in museum_name or \
                'Chongqing Museum of Natural History' in museum_name or\
                "Mevlana Museum" in museum_name or \
                "Tokyo Metropolitan Art Museum" in museum_name or\
                "Chengdu Museum" in museum_name or \
                "Royal Museums Greenwich" in museum_name or \
                "National Museum of Nature and Science" in museum_name or\
                "Suzhou Museum" in museum_name or \
                "Three Gorges Museum" in museum_name or\
                "Russian Museum" in museum_name:

                #bad website can not extract it is information, missing data case
                #escape it
                continue;

            # invalid case, page does not exist
            if "Reina Sofía" in museum_name or \
                "National Art Center" in museum_name or\
                "Museo Nacional de Historia" in museum_name or \
                "NGV International" in museum_name:
                continue

            text, redirect_page = extractor.USE_REQUEST(museum_name, True)
            if redirect_page:
                museum_name = text.split('[[')[1].split(']]')[0]
                text = extractor.USE_REQUEST(museum_name, True)[0]

            extracted_museum_infos = Parser_instance.run_function(ParserGenerator.parser_types['infobox'],text,logger)
            #Remove all special characters, punctuation and spaces from string
            import re
            new_name = re.sub('[^A-Za-z0-9]+', '', museum_name)

            file_name = new_name + "_info.txt"
            full_path = util.get_full_output_path(file_name)

            if len(extracted_museum_infos)>0:
                with open(full_path, "w", encoding="utf-8") as file:
                    for key, value in extracted_museum_infos.items():
                        file.write(key + ": " + value + "\n")

            # save city and one of its museums in a database
            extracted_city_infos["name"]= parsed_table[i][TableParser.column_type["city"]]
            extracted_museum_infos["name"] = parsed_table[i][TableParser.column_type["museum"]]
            extracted_museum_infos["visitors"] = parsed_table[i][TableParser.column_type["visitor"]]
            extracted_museum_infos["year"] = parsed_table[i][TableParser.column_type["year"]]

            city_visitor_info = df_parsed_table_2[df_parsed_table_2['city'] == extracted_city_infos["name"]]
            if extracted_city_infos["name"] == "Paris":
                print("shima")
            if(len(city_visitor_info) > 0):
                extracted_city_infos["city_visitor"] = city_visitor_info["city_visitor"].to_string(index=False)
                extracted_city_infos["city_visitor_reported_year"] = city_visitor_info["city_visitor_reported_year"].to_string(index=False)

            argument_list = {'city': extracted_city_infos, "museum":extracted_museum_infos}  # percent of original size
            datbase_manager = DatabaseManager.instance()
            datbase_manager.save(**argument_list)

