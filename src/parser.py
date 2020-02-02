#user define imports
import src.config as config
import src.util as util

#python imports
from abc import ABC, abstractmethod
import pandas

class Parser():
    def __init__(self):
        return

    @abstractmethod
    def do_parsing(self, text, do_debug):
        raise AssertionError("invalid call!")

class TableParser(Parser):
    def __init__(self):
        super().__init__()

    def do_parsing(self,text, do_debug):
        print("parsing table text!")
        import wikitextparser as wtp
        parsed = wtp.parse(text)
        table_info = parsed.tables[0].data()

        file_name = "List_of_most_visited_museums_table.txt"
        full_path = util.get_full_output_path(file_name)

        text_file = open(full_path, "w",encoding="utf-8")
        parsed_table = []
        column_type = {"museum":0,"city":1,"visitor":2,"year":3}
        for row_index in range(1, len(table_info), 1):
            cells = table_info[row_index]
            if do_debug:
                print(cells)

            cell_info = ""
            row = []

            #extract data
            if "NGV International" in cells[column_type["museum"]]:
                print("shima")
            museum_info = cells[column_type["museum"]]
            city_info = cells[column_type["city"]]
            visitor_info = cells[column_type["visitor"]]
            year_info = cells[column_type["year"]]

            # perform cleanup only after headers
            museum_info_2 = None
            if row_index>1:
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
                city_info = city_info.split("[[")[1].split(']]')[0]
                year_info = year_info.split('<ref')[0]

            cell_info = museum_info + " , "+ \
                        city_info + " , " + \
                        visitor_info + " , " + \
                        year_info + " , "

            if museum_info_2 is not None:
                cell_info = museum_info_2 + " , " + \
                            city_info + " , " + \
                            visitor_info + " , " + \
                            year_info + " , "

            row.append(museum_info)
            row.append(city_info)
            row.append(visitor_info)
            row.append(year_info)

            # save data
            parsed_table.append(row)

            if museum_info_2 is not None:
                row = []
                row.append(museum_info_2)
                row.append(city_info)
                row.append(visitor_info)
                row.append(year_info)

                # save data
                parsed_table.append(row)

            text_file.write(cell_info)
            text_file.write("\n")
        text_file.close()
        return parsed_table


class CityParser(Parser):
    def __init__(self):
        super().__init__()

    def do_parsing(self, text, do_debug):
        print("parsing city page text!")
        import wikitextparser as wtp
        parsed = wtp.parse(text)
        extracted_data = {}
        for template in parsed.templates:
            if 'infobox' in template.name.lower() or\
                'infobox settlement' in template.name.lower() or\
                'infobox country' in template.name.lower() or\
                'Infobox Russian federal subject' in template.name.lower():
               city_info = template.string
               import re
               found = ''
               try:
                   found = re.search('population(.*?)|', city_info)
                   key = "population_total"
                   value = ""
                   if key in city_info:
                       value = city_info.split(key)[1].split('\n')[0]
                       value.replace("=","")
                   extracted_data [key] = value

               except AttributeError:
                   # AAA, ZZZ not found in the original string
                   found = ''  # apply your error handling
               if do_debug:
                   print(city_info)
                   file_name = "city_info.txt"
                   full_path = util.get_full_output_path(file_name)

                   text_file = open(full_path, "w", encoding="utf-8")
                   text_file.write(city_info)
                   text_file.close()
               return city_info, extracted_data


        if len(extracted_data)==0:
            raise AssertionError("invalid case, extracted_data is empty!")
        return

class MuseumParser(Parser):
    def __init__(self):
        super().__init__()

    def do_parsing(self, text, do_debug):
        print("parsing museum page text!")
        import wikitextparser as wtp
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

               if do_debug:
                   print(museum_info)
                   file_name = "museum_info.txt"
                   full_path = util.get_full_output_path(file_name)
                   text_file = open(full_path, "w", encoding="utf-8")
                   text_file.write(museum_info)
                   text_file.close()
               return museum_info, extracted_data

        if len(extracted_data)==0:
            raise AssertionError("invalid case, extracted_data is empty!")
        return

