import sys, os
import re
import requests

import operator

import logging
logger = logging.getLogger(__name__)

root = "/Volumes/Download"

IMDB_URL_REGEX = re.compile(r'^http://www.imdb.com/title/(tt[0-9]+)/$',
                            re.IGNORECASE)
IMDB_ID_REGEX = re.compile(r'(tt\d{7})')

SEASON_NAME_REGEX = re.compile(r'(S\d\d?E\d\d?)', re.IGNORECASE)
WHOLE_SEASON_REGEX = re.compile(r'(Season.?\d+)', re.IGNORECASE)
HD_RES_REGEX = re.compile(r'^(.*)((?:480|720|1080)(?:p|i))', re.IGNORECASE)
TITLE_AND_YEAR_REGEX = re.compile(r'^(.*) (\d{0,4})')


def main():
    movies = []
    tv = []
    other = []

    for f in os.listdir(root):
        full_path = os.path.join(root, f)

        if os.path.isdir(full_path):
            nfos = find_nfos(full_path)
            ids = [extract_imdb_id(nfo) for nfo in nfos]
            omdb_responses = filter(None, [omdbapi(imdb=i) for i in ids])
            omdb_types = map(operator.itemgetter('Type'), omdb_responses)

            if 'movie' in omdb_types:
                movies.append(f)
                continue

            elif set(['episode', 'series']).intersection(omdb_types):
                tv.append(f)
                continue

        if detect_tv(root, f):
            tv.append(f)
            continue

        if detect_movie(root, f):
            movies.append(f)
            continue

        other.append(f)

    print_report(movies=movies, tv=tv, other=other)


def detect_movie(root, f):
    match = HD_RES_REGEX.search(f)
    if match:
        resolution = match.group(2)
        parts = re.split('[-_. ]', match.group(1))
        title_and_year = ' '.join(filter(None, parts))

        omdb = omdbapi(title=title_and_year)
        if omdb:
            print omdb


def detect_tv(root, f):
    return has_season_in_name(f)



def find_nfos(directory):
    return [os.path.join(directory, f) for f in os.listdir(directory)
            if f.endswith('.nfo')]

def extract_imdb_id(nfo_file):
    with open(nfo_file, 'r') as f:
        data = f.read()
        match = IMDB_URL_REGEX.search(data)
        if match:
            return match.group(1)

        match = IMDB_ID_REGEX.search(data)
        if match:
            return match.group(1)

def has_season_in_name(path):
    return SEASON_NAME_REGEX.search(path)

def print_report(movies, tv, other):
    print_list('Movies', movies)
    print_list('TV', tv)
    print_list('Other', other)

def print_list(label, items):
    print label
    print "---------------------"
    for m in items:
        print m
    print ""


def omdbapi(title=None, imdb=None):
    if not (title or imdb):
        return None

    params = dict(t=title, i=imdb)
    resp = requests.get("http://www.omdbapi.com", params=params)
    try:
        return resp.json()
    except:
        logger.error("omdb error:")
        for line in r.iter_lines():
            logger.error(line)

    return None



if __name__ == "__main__":
    main()
