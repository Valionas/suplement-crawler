import pymongo

def start_db_client(connection_string):
    return pymongo.MongoClient(connection_string)