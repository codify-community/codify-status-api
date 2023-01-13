import os

from pymongo import MongoClient

def mongoConnect():
    uri = os.environ.get('DATABASE_ADDRESS', None)
    return MongoClient(uri)
