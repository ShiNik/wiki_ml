# user define imports
from my_package import util as util
from my_package.log_manager import LogManager

# python imports
import wikitextparser as wtp
from abc import ABC, abstractmethod
import pandas as pd


class Parser:
    def __init__(self):
        return

    @abstractmethod
    def do_parsing(self, text):
        raise AssertionError("invalid call!")


class TableParser(Parser):
    # static data member
    column_type = {"museum": 0, "city": 1, "visitor": 2, "year": 3}

    def __init__(self):
        super().__init__()

    def do_parsing(self, text):
        logger = LogManager.instance()
        logger.log("Parsing table text!", logger.Logging_Levels["DEBUG"])

        parsed = wtp.parse(text)
        table_info = parsed.tables[0].data()

        df_parsed_table = pd.DataFrame(columns=TableParser.column_type.keys())
        for row_index in range(1, len(table_info), 1):
            cells = table_info[row_index]
            if logger.debug_enabled():
                logger.log(str(cells), logger.Logging_Levels["DEBUG"])

            # extract data
            museum_info = cells[TableParser.column_type["museum"]]
            city_info = cells[TableParser.column_type["city"]]
            visitor_info = cells[TableParser.column_type["visitor"]]
            year_info = cells[TableParser.column_type["year"]]

            # perform cleanup only after headers
            museum_info_2 = None
            if row_index > 1:
                city_info = city_info.split("[[")[1].split(']]')[0]
                year_info = year_info.split('<ref')[0]
                # post-process museum information
                if "[[" in museum_info:
                    museum_info = museum_info.split("[[")[1].split(']]')[0]
                    if "|" in museum_info:
                        # This can happen when we have 2 language like the case of Mexico City:
                        # '[[Museo Nacional de Historia|National Museum of History]]'
                        # best solution is to add 2 records
                        result = museum_info.split("|")
                        museum_info = result[0]
                        museum_info_2 = result[1]
                elif "|" in museum_info:
                    museum_info = museum_info.split("|")[1].split('|')[0]

            # save data
            df_parsed_table = df_parsed_table.append(
                pd.Series([museum_info, city_info, visitor_info, year_info], index=TableParser.column_type.keys()),
                ignore_index=True)
            if museum_info_2 is not None:
                df_parsed_table = df_parsed_table.append(pd.Series([museum_info_2, city_info, visitor_info, year_info],
                                                                   index=TableParser.column_type.keys()),
                                                         ignore_index=True)

        if logger.debug_enabled():
            file_name = "List_of_most_visited_museums_table.csv"
            full_path = util.get_full_output_path(file_name)
            df_parsed_table.to_csv(full_path, index=None, header=True)
        return df_parsed_table


class InfoboxParser(Parser):
    def __init__(self):
        super().__init__()

    def do_parsing(self, text):
        logger = LogManager.instance()
        logger.log("Parsing city page text!", logger.Logging_Levels["DEBUG"])

        parsed = wtp.parse(text)
        extracted_data = {}
        for template in parsed.templates:
            if 'infobox' in template.name.lower() or \
                    'infobox settlement' in template.name.lower() or \
                    'infobox country' in template.name.lower() or \
                    'Infobox Russian federal subject' in template.name.lower():
                city_info = template.string
                city_info_list = city_info.split("\n")
                for info in city_info_list:
                    if "|" in info and "=" in info:
                        key = info.split("|")[1].split('=')[0]
                        key = key.strip()

                        value = info.split("=")[1]
                        if "]]" in value and "[[" in value:
                            value = value.split("[[")[1].split(']]')[0]

                        extracted_data[key] = value

                if logger.debug_enabled():
                    print(city_info)
                    file_name = "city_info.txt"
                    full_path = util.get_full_output_path(file_name)
                    with open(full_path, "w", encoding="utf-8") as file:
                        file.write(city_info)

                return extracted_data

        if len(extracted_data) == 0:
            logger.log("invalid case, extracted_data is empty!!", logger.Logging_Levels["ERROR"])
        return extracted_data
