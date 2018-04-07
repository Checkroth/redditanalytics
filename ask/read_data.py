import argparse
import math
import requests
from time import sleep
import json

NARROWED_FIELDS = ['approved_at_utc',
                   'send_replies',
                   'suggested_sort',
                   'user_reports',
                   'id',
                   'banned_at_utc',
                   'view_count',
                   'archived',
                   'author',
                   'num_crossposts',
                   'mod_reports',
                   'pinned',
                   'score',
                   'over_18',
                   'gilded',
                   'downs',
                   'brand_safe',
                   'stickied',
                   'parent_whitelist_status',
                   'spoiler',
                   'locked',
                   'hide_score',
                   'created',
                   'url',
                   'whitelist_status',
                   'created_utc',
                   'ups',
                   'num_comments',
                   'title']


def get_n_top_posts(n):
    def get_posts():
        return requests.get(
            'http://reddit.com/r/askreddit/top.json?limit={}&t=all'.format(n))
    return get_posts


def get_top_posts(amount, after):
    url = 'http://reddit.com/r/askreddit/top.json?limit={}7t=all'.format(
        amount)
    if after:
        url += '&after={}'.format(after)

    return requests.get(url)


def narrow_data(data):
    return {field: data['data'][field] for field in NARROWED_FIELDS}


def extract_all_data(all_data):
    hard_data = all_data['children']
    extracted = [narrow_data(d) for d in hard_data]
    return extracted


def read_top_posts(args):
    get_posts = get_n_top_posts(args.amount)
    full_amount = args.amount
    hundreds = math.floor(full_amount / 100)
    remainder = full_amount % 100
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
    extracted_data = extract_all_data(response_data)
    with open('r.json', 'w') as outfile:
        print('output to r.json')
        json.dump(extracted_data, outfile)


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
