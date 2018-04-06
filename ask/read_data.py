import argparse
import requests
from time import sleep
import json


def get_n_top_posts(n):
    def get_posts():
        return requests.get(
            'http://reddit.com/r/askreddit/top.json?limit={}&t=all'.format(n))
    return get_posts


def read_top_posts(args):
    get_posts = get_n_top_posts(args.amount)
    reddit_response = get_posts()
    attempts = 1
    while reddit_response.status_code == 429 and attempts < 6:
        sleep(2)
        print('Too many requests, attempt number {}'.format(attempts))
        reddit_response = get_posts()
        attempts += 1

    if reddit_response.status_code == 429:
        raise Exception('Couldn\t pull data, too many requests')
    elif reddit_response.status_code != 200:
        raise Exception('Couldn\t pull data, code {}'
                        .format(reddit_response.status_code))

    response_data = json.loads(reddit_response.text)['data']
    with open('r.json', 'w') as outfile:
        print('output to r.json')
        json.dump(response_data, outfile)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    read_top_posts_parser = subparsers.add_parser('read_top_posts')
    read_top_posts_parser.add_argument(
        'amount',
        type=int)
    read_top_posts_parser.set_defaults(func=read_top_posts)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
