import re
import os

IMDB_URL_REGEX = re.compile(r'^http://www.imdb.com/title/(tt[0-9]+)/$',
                            re.IGNORECASE)
IMDB_ID_REGEX = re.compile(r'(tt\d{7})')


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

