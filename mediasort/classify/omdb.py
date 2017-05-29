import requests

import logging
logger = logging.getLogger(__name__)

class Omdb(object):

    def __init__(self, config):
        self.config = config

    def api(self, title=None, imdb=None, year=None):
        if not (title or imdb):
            return None

        params = dict(t=title, i=imdb, y=year)
        resp = requests.get("http://www.omdbapi.com", params=params)
        try:
            answer = resp.json()
            response_val = answer.get('Response')
            if response_val == 'True':
                return answer

            elif response_val == 'False':
                logger.error('[OMDB] Error: %s (from %s)' % (
                    answer.get('Error'), params
                ))
            else:
                logger.error('[OMDB] Unknown: %s (from %s)' % (answer, params))

            return None

        except:
            logger.error("[OMDB] Request error:")
            for line in r.iter_lines():
                logger.error(line)

        return None


