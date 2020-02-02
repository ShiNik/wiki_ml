#user define imports
import src.config as config
import src.util as util
from  src.log_manager import LogManager

#python imports
import wikitextparser as wtp
from abc import ABC, abstractmethod
import pandas as pd

class Parser():
    def __init__(self):
        return
    @abstractmethod
    def do_parsing(self, text, do_debug):
        raise AssertionError("invalid call!")

class TableParser(Parser):
    def __init__(self):
        super().__init__()

    def do_parsing(self,text, logger):
        logger.log("Parsing table text!", LogManager.Logging_Levels["DEBUG"])

        parsed = wtp.parse(text)
        table_info = parsed.tables[0].data()

        column_type = {"museum":0,"city":1,"visitor":2,"year":3}
        df_parsed_table = pd.DataFrame(columns = column_type.keys())
        for row_index in range(1, len(table_info), 1):
            cells = table_info[row_index]
            if logger.debug_enabled():
                logger.log(str(cells), LogManager.Logging_Levels["DEBUG"])

            #extract data
            museum_info = cells[column_type["museum"]]
            city_info = cells[column_type["city"]]
            visitor_info = cells[column_type["visitor"]]
            year_info = cells[column_type["year"]]

            # perform cleanup only after headers
            museum_info_2 = None
            if row_index>1:
                city_info = city_info.split("[[")[1].split(']]')[0]
                year_info = year_info.split('<ref')[0]
                #post-process museume information
                if "[[" in museum_info:
                    museum_info = museum_info.split("[[")[1].split(']]')[0]
                    if "|" in museum_info:
                        # This can happen when we have 2 language like te case of Mexico City:
                        #'[[Museo Nacional de Historia|National Museum of History]]'
                        # best solution to add 2 records
                        result = museum_info.split("|")
                        museum_info = result[0]
                        museum_info_2 = result[1]
                elif "|" in museum_info:
                    museum_info = museum_info.split("|")[1].split('|')[0]

            # save data
            df_parsed_table = df_parsed_table.append(pd.Series([museum_info,city_info,visitor_info,year_info], index = column_type.keys()), ignore_index=True)
            if museum_info_2 is not None:
                df_parsed_table = df_parsed_table.append(pd.Series([museum_info_2, city_info, visitor_info, year_info], index=column_type.keys()), ignore_index=True)

        if logger.debug_enabled():
            file_name = "List_of_most_visited_museums_table.csv"
            full_path = util.get_full_output_path(file_name)
            df_parsed_table.to_csv(full_path, index = None, header=True)
        return df_parsed_table


class CityParser(Parser):
    def __init__(self):
        super().__init__()

    def do_parsing(self, text, logger):
        logger.log("Parsing city page text!", LogManager.Logging_Levels["DEBUG"])

        parsed = wtp.parse(text)
        extracted_data = {}
        for template in parsed.templates:
            if 'infobox' in template.name.lower() or\
                'infobox settlement' in template.name.lower() or\
                'infobox country' in template.name.lower() or\
                'Infobox Russian federal subject' in template.name.lower():
                city_info = template.string
                key = "population_total"
                value = ""
                if key in city_info:
                   value = city_info.split(key)[1].split('\n')[0]
                   value.replace("=", "")
                extracted_data[key] = value

                if logger.debug_enabled():
                    print(city_info)
                    file_name = "city_info.txt"
                    full_path = util.get_full_output_path(file_name)

                    text_file = open(full_path, "w", encoding="utf-8")
                    text_file.write(city_info)
                    text_file.close()

                return city_info, extracted_data

        if len(extracted_data)==0:
            logger.log("invalid case, extracted_data is empty!!", LogManager.Logging_Levels["ERROR"])
        return

class MuseumParser(Parser):
    def __init__(self):
        super().__init__()

    def do_parsing(self, text, logger):
        logger.log("Parsing museum page text!", LogManager.Logging_Levels["DEBUG"])

        parsed = wtp.parse(text)
        extracted_data = {}
        for template in parsed.templates:
            if 'infobox' in template.name.lower() or \
                'infobox museum' in template.name.lower():
               museum_info = template.string

               key = "name"
               value = ""
               if key in museum_info:
                   value = museum_info.split(key)[1].split('\n')[0]
                   value.replace("=", "")
               extracted_data [key] = value

               key = "established"
               value = ""
               if key in museum_info:
                   value = museum_info.split(key)[1].split('\n')[0]
                   value.replace("=", "")
               extracted_data [key] = value

               key = "type"
               value = ""
               if key in museum_info:
                   value = museum_info.split(key)[1].split('\n')[0]
                   value.replace("=", "")
               extracted_data [key] = value

               key = "visitors"
               value = ""
               if key in museum_info:
                   value = museum_info.split(key)[1].split('\n')[0]
                   value.replace("=", "")
               extracted_data [key] = value

               key = "location"
               value = ""
               if key in museum_info:
                   value = museum_info.split(key)[1].split('\n')[0]
                   value.replace("=", "")
               extracted_data [key] = value

               key = "collections"
               value = ""
               if key in museum_info:
                   value = museum_info.split(key)[1].split('\n')[0]
                   value.replace("=", "")
               extracted_data [key] = value

               key = "collection_size"
               value = ""
               if key in museum_info:
                   value = museum_info.split(key)[1].split('\n')[0]
                   value.replace("=", "")
               extracted_data [key] = value

               if logger.debug_enabled():
                   print(museum_info)
                   file_name = "museum_info.txt"
                   full_path = util.get_full_output_path(file_name)
                   text_file = open(full_path, "w", encoding="utf-8")
                   text_file.write(museum_info)
                   text_file.close()
               return museum_info, extracted_data

        if len(extracted_data)==0:
            logger.log("invalid case, extracted_data is empty!!", LogManager.Logging_Levels["ERROR"])
        return

