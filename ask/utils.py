import json


def get_reddit_data(filename):
    with open(filename, 'r') as infile:
        data = json.load(infile)
        yield data
