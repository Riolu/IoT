from pymongo import MongoClient
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('dbnames', nargs='+', type=str, help='name(s) of database(s) to drop')
    args = parser.parse_args()

    client = MongoClient('localhost', 27017)

    for dbname in args.dbnames:
        client.drop_database(dbname)