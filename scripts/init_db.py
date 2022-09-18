#!/usr/bin/sudo /usr/bin/python
import json
import os
import sys
from typing import List

import pymongo

sys.path += [os.getcwd()]

database = 'sge'

client = pymongo.MongoClient('mongodb://root:root@mongo:27017/?retryWrites=true&w=majority')


def get_json_data(filepath: str) -> List[dict]:
    """Return validated faces data loaded from filepath."""
    with open(filepath) as f:
        return json.load(f)


def db_initialized() -> bool:
    """Verifica se o banco de dados já foi inicializado."""
    for db in client.list_databases():
        if db['name'] == database:
            return True
    return False


def populate_db(data: List[dict], collection: str):
    """Insere dados iniciais para popular o banco de dados."""
    db = client[database]
    db[collection].insert_many(data)


if __name__ == '__main__':
    if db_initialized():
        print(f'Pulando carregamento dos dados. O banco {database} já foi inicializado.')
        sys.exit(0)

    COLLECTIONS = ['regionals', 'areas', 'employees']

    for collection in COLLECTIONS:
        FIXTURE_DATA_FILEPATH = f'tests/fixtures/{collection}.json'
        regionals_collection = 'regionals'
        print(f'Populando a collection {collection}...')
        data = get_json_data(FIXTURE_DATA_FILEPATH)
        populate_db(data, collection)
