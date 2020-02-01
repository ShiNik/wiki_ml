from scripts.userscripts import parser as prs

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

    def run_function(self, parser_type, text, do_debug=False):
        return  self.fActive[parser_type].do_parsing(text, do_debug)

# class GenerateTrainer:
#     def __init__(self,training_type):
#         self.fActive = self.generate_trainer(training_type) # mapping: string --> variable = function name
#
#     def generate_trainer(self, training_type):
#         switcher = {
#             'gs': grid_search,
#             't': train
#         }
#
#         trainer = switcher.get(training_type.lower(), None)
#
#         if trainer == None:
#             raise AssertionError("training_type is invalid!")
#
#         return trainer
#
#     def run_function(self, in_model_generater, in_config, training_data):
#         self.fActive(in_model_generater, in_config, training_data)
#
# class GeneratePredicter:
#     def __init__(self, predicting_type):
#         self.fActive = self.generate_predicter(predicting_type) # mapping: string --> variable = function name
#
#     def generate_predicter(self, predicting_type):
#         switcher = {
#             'p': self.predict,
#             'c': self.cam_predict
#         }
#
#         predicter = switcher.get(predicting_type.lower(), None)
#
#         if predicter == None:
#             raise AssertionError("predicting_type is invalid!")
#
#         return predicter
#
#     def predict(self):
#             test_model_path = get_path(config.model_path_root, 'no_cam\\Model-60-0.820.model')
#             test_data_path = get_path(config.data_path_root, 'test')
#             simple_cnn.predict(test_data_path, test_model_path, config)
#
#     def cam_predict(self, config):
#         test_model_path = get_path(config.model_path_root, 'Vgg_16_Cam\\Model-02-0.978.model')
#         test_data_path = get_path(config.data_path_root, 'test\\cam')
#         cam.predict(test_data_path, test_model_path, config.image_size)
#
#     def run_function(self, config):
#         self.fActive(config)



