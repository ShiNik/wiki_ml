#user define imports
from src.factory import ParserGenerator as ParserGenerator
import src.wiki_extractor as extractor
import src.util as util
from  src.log_manager import LogManager

#step 1: parse the main page : List_of_most_visited_museums
#step 2: generate the table
#spet 3: parse the musium page
#step 4: extract musium information
#spet 5: parse the city page
#step 6: extract city information

def main():
    logger = LogManager()
    logger.log("Staring the application!", LogManager.Logging_Levels["DEBUG"])

    page_name = "List of most visited museums"
    section_id = "2"
    # page_name = "Louvre"
    parser_list = [ParserGenerator.parser_types['table'], ParserGenerator.parser_types['city'], ParserGenerator.parser_types['museum']]
    Parser_instance = ParserGenerator(parser_list)

    # text = USE_WIKI_BOT(page_name)
    text = extractor.USE_REQUEST(page_name)

    df_parsed_table = Parser_instance.run_function(ParserGenerator.parser_types['table'],text, logger)

    parsed_table = df_parsed_table.values.tolist()
    PRINT_TABLE = False
    if PRINT_TABLE:
        for cell in parsed_table[0]:
            print(cell)
        for row in parsed_table:
            print(*row)

    for i in range(1, len(parsed_table), 1):
        city_name = parsed_table[i][1]
        print(city_name)
        text = extractor.USE_REQUEST(city_name, True)
        redirect_page = False
        if redirect_page:
            city_name = text.split('[[')[1].split(']]')[0]
            text = extractor.USE_REQUEST(city_name, True)[0]

        if 'Mexico City' in city_name:
            print("shima")
        parsed_city, extracted_data = Parser_instance.run_function(ParserGenerator.parser_types['city'],text,logger)

        file_name = city_name + "_info.txt"
        full_path = util.get_full_output_path(file_name)

        text_file = open(full_path , "w", encoding="utf-8")
        for key, value in extracted_data.items():
            text_file.write(key + ": " + value + "\n")

        text_file.write(parsed_city)
        text_file.close()

        musiume_name = parsed_table[i][0]
        print(musiume_name)

        if "National Gallery of Victoria" in musiume_name:
            print("shima")

        #I might look at categor for "Tokyo Metropolitan Art Museum"
        #there I might have link to real website
        # Category: National Museum of Nature and Science
        if 'Zhejiang Museum' in musiume_name or \
            'Chongqing Museum of Natural History' in musiume_name or\
            "Mevlana Museum" in musiume_name or \
            "Tokyo Metropolitan Art Museum" in musiume_name or\
            "Chengdu Museum" in musiume_name or \
            "Royal Museums Greenwich" in musiume_name or \
            "National Museum of Nature and Science" in musiume_name or\
            "Suzhou Museum" in musiume_name or \
            "Three Gorges Museum" in musiume_name or\
            "Russian Museum" in musiume_name:

            #bad website can not extract it is information, missing data case
            #escape it
            continue;

        # invalid case, page does not exist
        if "Reina Sofía" in musiume_name or \
            "National Art Center" in musiume_name or\
            "Museo Nacional de Historia" in musiume_name or \
            "NGV International" in musiume_name:
            continue

        text = extractor.USE_REQUEST(musiume_name, True)
        redirect_page = False
        if redirect_page:
            musiume_name = text.split('[[')[1].split(']]')[0]
            text = extractor.USE_REQUEST(musiume_name, True)[0]

        parsed_musiume, extracted_data = Parser_instance.run_function(ParserGenerator.parser_types['museum'],text,logger)
        #Remove all special characters, punctuation and spaces from string
        import re
        new_name = re.sub('[^A-Za-z0-9]+', '', musiume_name)

        file_name = new_name + "_info.txt"
        full_path = util.get_full_output_path(file_name)

        text_file = open(full_path , "w", encoding="utf-8")
        for key, value in extracted_data.items():
            text_file.write(key + ": " + value + "\n")
        text_file.write(parsed_musiume)
        text_file.close()


main()