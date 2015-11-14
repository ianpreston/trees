import click
import requests


def fetch_frontpage(after):
    r = requests.get(
        'https://api.reddit.com/r/trees/new',
        params={
            'after': after,
        },
        headers={
            'User-Agent': 'trees /u/evilyomeil',
        },
    )
    r.raise_for_status()
    return r.json()


def get_authors():
    usernames = set()
    after = None
    for x in xrange(10):
        j = fetch_frontpage(after)

        after = j['data']['after']
        authors = set(link['data']['author'] for link in j['data']['children'])
        usernames |= set(authors)

    return usernames


@click.command()
def main():
    usernames = get_authors()
    with open('usernames.txt', 'w') as f:
        f.write('\n'.join(usernames))


if __name__ == '__main__':
    main()
