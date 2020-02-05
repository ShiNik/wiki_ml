#user define imports

#python imports
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.inspection import inspect
import pandas as pd

Base = declarative_base()
class City(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    population = Column(String)
    size = Column(String)
    year_reported = Column(String)

    def __init__(self, city_infos):
        super().__init__()
        self.name = city_infos["name"]

        key ="population_total"
        if key in city_infos:
            self.population = city_infos[key]

        key ="area_total_km2"
        if key in city_infos:
            self.size = city_infos[key]

        key ="population_as_of"
        if key in city_infos:
            self.year_reported = city_infos[key]

    def is_valid(self):
        # todo: modify this to be depend on user needs
        return (self.population != None and self.name != None)

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

        key ="type"
        if key in museum_infos:
            self.type = museum_infos[key]

        key ="publictransit"
        if key in museum_infos:
            self.public_transit = museum_infos[key]

        key ="location"
        if key in museum_infos:
            self.location = museum_infos[key]

        key ="established"
        if key in museum_infos:
            self.established = museum_infos[key]

        key ="built"
        if key in museum_infos:
            self.built = museum_infos[key]

        self.city_id = city_id

    def is_valid(self):
        # todo: modify this to be depend on user needs
        return (self.visitor != None and self.name != None)

    def to_dict(self):
        return self.__dict__

class Singleton:
    """
    A non-thread-safe helper class to ease implementing singletons.
    This should be used as a decorator -- not a metaclass -- to the
    class that should be a singleton.

    The decorated class can define one `__init__` function that
    takes only the `self` argument. Also, the decorated class cannot be
    inherited from. Other than that, there are no restrictions that apply
    to the decorated class.

    To get the singleton instance, use the `instance` method. Trying
    to use `__call__` will result in a `TypeError` being raised.

    """

    def __init__(self, decorated):
        self._decorated = decorated

    def instance(self):
        """
        Returns the singleton instance. Upon its first call, it creates a
        new instance of the decorated class and calls its `__init__` method.
        On all subsequent calls, the already created instance is returned.

        """
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)

@Singleton
class DatabaseManager():
    # # static data member
    # database_type = {"postgres": "postgres"}

    def __init__(self):
        self.database_type = {"postgres": "postgres"}
        return

    def init(self, config ):
        if config.database_type not in self.database_type:
            raise AssertionError("currently " + config.database_type + " database does not supported by the system!")

        # build connection string
        db_string = config.database_type + "://" + config.database_user_name + ":" + \
                    config.database_password + "@" + config.database_host + ":" +\
                    config.database_port + "/" + config.database_name

        self.db_engine = create_engine(db_string)

        Session = sessionmaker(bind=self.db_engine)
        self.session = Session()

        self.metadata = Base.metadata
        self.metadata.bind = self.db_engine
        if config.delete_tables:
            self.drop_table(Museum.__tablename__)
            self.drop_table(City.__tablename__)


        self.metadata.create_all(self.db_engine)

    def save(self, **data):
        if not isinstance(data, dict):
            raise AssertionError("data should be provided as a dict")
        if len(data)==0:
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

            museum_infos["name"]= "tehran"
            new_museum_2 = Museum(museum_infos, new_city.id)
            self.session.add(new_museum_2)
            # save data to the database
            self.session.commit()

            # debug code
            # print(self.session.new)

        except ProgrammingError as E:
            print(E.args[0])
            raise E.args[0]

    # def query_to_list(self, rset):
    #     """List of result
    #     Return: columns name, list of result
    #     """
    #     result = []
    #     for obj in rset:
    #         instance = inspect(obj)
    #         items = instance.attrs.items()
    #         result.append([x.value for _, x in items])
    #     return instance.attrs.keys(), result
    #
    # def query_to_dict(self, rset):
    #     result = defaultdict(list)
    #     for obj in rset:
    #         instance = inspect(obj)
    #         for key, x in instance.attrs.items():
    #             result[key].append(x.value)
    #     return result

    def object_as_dict(self, obj):
        return {c.key: getattr(obj, c.key)
                for c in inspect(obj).mapper.column_attrs}

    def keys_swap(self,orig_key, new_key, d):
        d[new_key] = d.pop(orig_key)

    def query_to_df(self,rset):
        data_list = self.query_to_list(rset)
        keys = data_list[0].keys()
        df_parsed_table = pd.DataFrame(columns=keys)
        for data in data_list:
            values = list(data.values())
            df_parsed_table=df_parsed_table.append(pd.Series(values, index=keys), ignore_index=True)
        return df_parsed_table

    def query_to_list(self, rset):
        result = []
        for row in rset:
            row_data = {}
            for object in row:
                object_in_dict = self.object_as_dict(object)
                self.keys_swap("name", object.__tablename__, object_in_dict)
                row_data.update(object_in_dict)
            result.append(row_data)

        return result

    def load(self):
        try:
            query_result = self.session.query(City, Museum).filter( Museum.city_id == City.id).all()
            return self.query_to_df(query_result)
        except ProgrammingError as E:
            print(E.args[0])
            raise E.args[0]

    def delete_all_data(self):
        self.session.query(Museum).delete()
        self.session.query(City).delete()
        self.session.commit()

    def drop_table(self,table_name):
        table = self.metadata.tables.get(table_name)
        if table is not None:
            # logging.info(f'Deleting {table_name} table')
            self.metadata.drop_all(self.db_engine, [table], checkfirst=True)

