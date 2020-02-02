import parser as prs

class ParserGenerator:
    def __init__(self,parser_types_to_generate):
        if not isinstance(parser_types_to_generate, list):
            raise AssertionError("parser_types_to_generate should be provided as a list")
        if len(parser_types_to_generate) == 0:
            raise AssertionError("parser_types_to_generate is empty!")

        self.fActive = self.generate_parsers(parser_types_to_generate) # mapping: string --> variable = function name

    #types
    parser_types = {'table': 'table', 'city': 'city', 'museum': 'museum'}

    def generate_parsers(self, parser_types_to_generate):
        switcher = {
            'table':   prs.TableParser(),
            'city':    prs.CityParser(),
            'museum':  prs.MuseumParser()
        }
        parsers_list = {}
        for parser in  parser_types_to_generate:
            type = ParserGenerator.parser_types[parser.lower()]
            current_parser = switcher.get(type, None)
            if current_parser == None:
                raise AssertionError("model_type is invalid!")
            parsers_list[type] =current_parser
        return parsers_list

    def run_function(self, parser_type, text, logger):
        return  self.fActive[parser_type].do_parsing(text, logger)
