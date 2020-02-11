# user define imports
from my_package.singleton import Singleton

# python imports
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.inspection import inspect
from sqlalchemy_utils import create_database, database_exists
import pandas as pd

Base = declarative_base()


class City(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    population = Column(String)
    size = Column(String)
    year_reported = Column(String)
    city_visitor = Column(String)
    city_visitor_reported_year = Column(String)

    def __init__(self, city_infos):
        super().__init__()
        self.name = city_infos["name"]

        key = "population_total"
        if key in city_infos:
            self.population = city_infos[key]

        key = "area_total_km2"
        if key in city_infos:
            self.size = city_infos[key]

        key = "population_as_of"
        if key in city_infos:
            self.year_reported = city_infos[key]

        key = "city_visitor"
        if key in city_infos:
            self.city_visitor = city_infos[key]

        key = "city_visitor_reported_year"
        if key in city_infos:
            self.city_visitor_reported_year = city_infos[key]

    def is_valid(self):
        # todo: modify this to be based on user needs
        return self.population is not None and self.name is not None

    def to_dict(self):
        return self.__dict__


class Museum(Base):
    __tablename__ = "museum"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    visitor = Column(String)
    year_reported = Column(String)
    type = Column(String)
    public_transit = Column(String)
    location = Column(String)
    established = Column(String)
    built = Column(String)
    city_id = Column(Integer, ForeignKey("city.id"))

    def __init__(self, museum_infos, city_id):
        super().__init__()

        self.name = museum_infos["name"]
        self.visitor = museum_infos["visitors"]
        self.year_reported = museum_infos["year"]

        key = "type"
        if key in museum_infos:
            self.type = museum_infos[key]

        key = "publictransit"
        if key in museum_infos:
            self.public_transit = museum_infos[key]

        key = "location"
        if key in museum_infos:
            self.location = museum_infos[key]

        key = "established"
        if key in museum_infos:
            self.established = museum_infos[key]

        key = "built"
        if key in museum_infos:
            self.built = museum_infos[key]

        self.city_id = city_id

    def is_valid(self):
        # todo: modify this to be depend on user needs
        return (self.visitor is not None and self.name is not None)

    def to_dict(self):
        return self.__dict__


@Singleton
class DatabaseManager():
    def __init__(self):
        self.database_type = {"postgres": "postgres"}
        self.initialized = False

    def init(self, config):
        if self.initialized:
            return

        if config.database_type not in self.database_type:
            raise AssertionError("currently " + config.database_type + " database does not supported by the system!")

        self.initialized = True

        # build connection string
        db_string = config.database_type + "://" + config.database_user_name + ":" + \
                    config.database_password + "@" + config.database_host + ":" + \
                    config.database_port + "/" + config.database_name

        if not database_exists(db_string):
            create_database(db_string)

        self.db_engine = create_engine(db_string)

        session = sessionmaker(bind=self.db_engine)
        self.session = session()

        self.metadata = Base.metadata
        self.metadata.bind = self.db_engine
        if config.delete_tables:
            self.drop_table(Museum.__tablename__)
            self.drop_table(City.__tablename__)

        self.metadata.create_all(self.db_engine)

    def save(self, **data):
        if not self.initialized:
            #todo: log database is not initialized
            return

        if not isinstance(data, dict):
            raise AssertionError("data should be provided as a dict")
        if len(data) == 0:
            raise AssertionError("data is empty!")
        try:
            city_infos = data['city']
            museum_infos = data['museum']

            new_city = City(city_infos)
            self.session.add(new_city)
            # save data to the database
            self.session.commit()

            new_museum = Museum(museum_infos, new_city.id)
            self.session.add(new_museum)
            # save data to the database
            self.session.commit()

            # debug code
            # print(self.session.new)

        except ProgrammingError as E:
            print(E.args[0])
            raise E.args[0]

    def object_as_dict(self, obj):
        return {c.key: getattr(obj, c.key)
                for c in inspect(obj).mapper.column_attrs}

    def keys_swap(self, orig_key, new_key, d):
        d[new_key] = d.pop(orig_key)

    def query_to_df(self, rset):
        data_list = self.query_to_list(rset)
        keys = data_list[0].keys()
        df_parsed_table = pd.DataFrame(columns=keys)
        for data in data_list:
            values = list(data.values())
            df_parsed_table = df_parsed_table.append(pd.Series(values, index=keys), ignore_index=True)
        return df_parsed_table

    def objects_valid(self, objects):
        for object in objects:
            if not object.is_valid():
                return False
        return True

    def query_to_list(self, rset):
        result = []
        for row in rset:
            row_data = {}
            if not self.objects_valid(row):
                continue

            for object in row:
                object.is_valid()
                object_in_dict = self.object_as_dict(object)
                self.keys_swap("name", object.__tablename__, object_in_dict)
                row_data.update(object_in_dict)
            result.append(row_data)

        return result

    def load(self):
        if not self.initialized:
            # todo: log database is not initialized
            return

        try:
            query_result = self.session.query(City, Museum).filter(Museum.city_id == City.id).all()
            return self.query_to_df(query_result)
        except ProgrammingError as E:
            print(E.args[0])
            raise E.args[0]

    def delete_all_data(self):
        if not self.initialized:
            # todo: log database is not initialized
            return

        self.session.query(Museum).delete()
        self.session.query(City).delete()
        self.session.commit()

    def drop_table(self, table_name):
        if not self.initialized:
            # todo: log database is not initialized
            return

        table = self.metadata.tables.get(table_name)
        if table is not None:
            # todo:  log (f'Deleting {table_name} table')
            self.metadata.drop_all(self.db_engine, [table], checkfirst=True)
