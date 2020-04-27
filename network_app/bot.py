import requests
import random
import string
import json
import sys
import os
from argparse import ArgumentParser
from requests.exceptions import HTTPError


def random_string(char_set, length):
    return ''.join(random.choice(char_set) for i in range(length))


# generates paragraph of 60 to 80 words
# each 3 to 10 letters length separated by whitespaces
def random_paragraph():
    return ' '.join((random_string(string.ascii_letters, random.randint(3, 10)) for _ in range(random.randint(60, 80))))


def signup_users(number, verbose):
    url = 'http://127.0.0.1:8000/api/v1/signup/'
    users = []
    for _ in range(number):
        credentials = {
            'username': random_string(string.ascii_lowercase, 8),
            'password': random_string(string.ascii_letters + string.digits, 12)
        }
        if verbose:
            print('creating user with the following credentials:', credentials)
        try:
            res = requests.post(url, data=credentials)
            res.raise_for_status()
            users.append(credentials)
            if verbose:
                print('success')
        except HTTPError as e:
            if verbose:
                print(f'error: {e}')
    return users


def login_user(credentials, verbose):
    url = 'http://127.0.0.1:8000/api/v1/login/'
    try:
        res = requests.post(url, data=credentials)
        res.raise_for_status()
        auth_data = json.loads(res.content.decode())
        return auth_data['token']
    except HTTPError as e:
        if verbose:
            print(f'couldn\'t get jwt token for user {credentials["username"]}, error: {e}')
        return None


def create_posts(users, max_posts, verbose):
    url = 'http://127.0.0.1:8000/api/v1/posts/'
    posts = []
    for user in users:
        bearer_token = login_user(user, verbose)
        if not bearer_token:
            continue
        num_posts = random.randint(1, max_posts)
        if verbose:
            print(f'creating {num_posts} post(s) for user {user["username"]}')
        for _ in range(num_posts):
            content = {'text': random_paragraph()}
            headers = {"Authorization": f"Bearer {bearer_token}"}
            try:
                res = requests.post(url, data=content, headers=headers)
                res.raise_for_status()
                post = json.loads(res.content.decode())
                posts.append(post["id"])
                if verbose:
                    print(f'successfully created, id: {post["id"]}')
            except HTTPError as e:
                if verbose:
                    print(f'couldn\'t publish post, error: {e}')
    return posts


def like_posts(users, posts, max_likes, verbose):
    posts_number = len(posts)
    for user in users:
        likes_number = random.randint(1, max_likes)
        posts_to_like = random.sample(range(0, posts_number), likes_number)
        if verbose:
            print(f'user {user["username"]} is going to like {likes_number} post(s)')
        bearer_token = login_user(user, verbose)
        if not bearer_token:
            continue
        for i in posts_to_like:
            post_id = posts[i]
            url = f'http://127.0.0.1:8000/api/v1/posts/{post_id}/like/'
            headers = {"Authorization": f"Bearer {bearer_token}"}
            try:
                res = requests.post(url, headers=headers)
                res.raise_for_status()
                if verbose:
                    print(f'post {post_id} successfully liked')
            except HTTPError as e:
                if verbose:
                    print(f'couldn\'t like post {post_id}, error: {e}')


def read_config(filename):
    try:
        with open(filename, 'r') as fd:
            num_users, max_posts, max_likes = (int(i) for i in fd.readline().split())
            return num_users, max_posts, max_likes
    except FileNotFoundError:
        print(f'Error: file {filename} not found')
        exit(0)
    except ValueError:
        print('Error: config should be provided in the following format:\n'
              '<number_of_users> <max_posts_per_user> <max_likes_per_user>')
        exit(0)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('config_file', nargs='?', action='store',
                        default=os.path.join(sys.path[0], 'config.txt'),
                        help='path to config file')
    parser.add_argument('-v', '--verbose', help='log performed actions to console',
                        default=False, action='store_true')
    args = parser.parse_args()

    number_of_users, max_posts_per_user, max_likes_per_user = read_config(args.config_file)
    users = signup_users(number_of_users, args.verbose)
    posts = create_posts(users, max_posts_per_user, args.verbose)
    max_likes_per_user = min(max_likes_per_user, len(posts))
    like_posts(users, posts, max_likes_per_user, args.verbose)
