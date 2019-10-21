# from pymongo import MongoClient
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('dbnames', nargs='+', type=str)
    args = parser.parse_args()
    print(args)

    # client = MongoClient('localhost', 27017)

    # client.drop_database()