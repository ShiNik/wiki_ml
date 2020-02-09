# General
log_path_root = 'logs'
output_path_root = 'output'

silent_mode_enabled = True

# Data
main_page_name = "List of most visited museums"

# Database
wiki_to_database_city_map = {"name": "name", "population_total": "population",
                             "area_total_km2": "size", "population_as_of": "year_reported",
                             "city_visitor": "city_visitor", "city_visitor_reported_year": "city_visitor_reported_year"}

wiki_to_database_museum_map = {"name": "name", "visitor": "visitor", "year": "year_reported",
                               "type": "type", "publictransit": "public_transit",
                               "location": "location", "established": "established",
                               "built": "built"}
database_name = "test"
database_type = "postgres"
database_user_name = "pguser"
database_password = "pguser"

# outside docker-compose
# database_host = localhost, ports are mapped from container to host
# from inside docker-compose
# database_host = pywikibot_dbpostgres_1 because docker-compose has its own network
database_host = "localhost"
database_port = "5432"

delete_tables = False
