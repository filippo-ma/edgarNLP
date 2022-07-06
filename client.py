import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from pyrate_limiter import RequestRate, Limiter
from constants import MAX_REQUESTS_PER_SECOND, MAX_RETRIES, BACKOFF_FACTOR



rate = RequestRate(MAX_REQUESTS_PER_SECOND, MAX_RETRIES)
limiter = Limiter(rate)


retry_strategy = Retry(
        total = MAX_RETRIES,
        backoff_factor = BACKOFF_FACTOR,
        status_forcelist = [403,429,500,502,503,504]
    )


class EdgarClient:
  
    def __init__(self, user: str):
        self.user = user
        self._session = requests.Session()
        


    @limiter.ratelimit(delay=True)
    def get_resp(self, url: str, params: dict = None):
            
        headers = {'User-Agent': self.user}

        with self._session as s:

            s.mount("https://", adapter=HTTPAdapter(max_retries=retry_strategy))
            resp = s.get(url, headers=headers) 
            resp_headers = resp.headers
            content_type = resp_headers['Content-Type']

            if content_type in ['application/atom+xml', 'text/xml', 'text/html']:
                return resp.content.decode('utf-8')
            else:
                return resp.json()
                