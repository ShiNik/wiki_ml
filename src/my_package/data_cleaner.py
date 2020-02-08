# python imports
import re


class DataCleaner:
    def __init__(self):
        return

    @staticmethod
    def clean_year(str_year):
        p = re.compile('(\d{4})')
        result_re = p.findall(str_year)
        return "" if len(result_re) == 0 else result_re[0]

    @staticmethod
    def clean_number(str_number):
        a = '\b(\d*,\d*)\b'
        b = '[^0-9]+'
        result_re = re.sub(b, '', str_number)
        return '' if len(result_re) == 0 else result_re

    @staticmethod
    def perform_cleanup(df):
        cleaned_df = df
        heads = {i: df.columns.get_loc(i) for i in df.columns}
        for i in range(len(df)):
            key = "population"
            if key in heads:
                population = cleaned_df.loc[i, key]
                cleaned_df.loc[i, key] = "" if not population else DataCleaner.clean_number(population)

            key = "visitor"
            if key in heads:
                visitor = cleaned_df.loc[i, key]
                cleaned_df.loc[i, key] = "" if not visitor else DataCleaner.clean_number(visitor)

            key = "year_reported"
            if key in heads:
                year = cleaned_df.loc[i, key]
                cleaned_df.loc[i, key] = "" if not year else DataCleaner.clean_year(year)

            key = "established"
            if key in heads:
                year = cleaned_df.loc[i, key]
                cleaned_df.loc[i, key] = "" if not year else DataCleaner.clean_year(year)

            key = "built"
            if key in heads:
                year = cleaned_df.loc[i, key]
                cleaned_df.loc[i, key] = "" if not year else DataCleaner.clean_year(year)

            key = "city_visitor"
            if key in heads:
                visitor = cleaned_df.loc[i, key]
                cleaned_df.loc[i, key] = "" if not visitor else DataCleaner.clean_number(visitor)

            # todo: add regex to cleanup
            key = "size"
            if key in heads:
                size = cleaned_df.loc[i, key]
                cleaned_df.loc[i, key] = size

        return cleaned_df
