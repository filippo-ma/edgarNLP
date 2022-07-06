ARCHIVE_DATA_ENDPOINT = "https://www.sec.gov/Archives/edgar/data"
SUBMISSIONS_API_ENDPOINT = "https://data.sec.gov/submissions"

MAX_REQUESTS_PER_SECOND = 10
MAX_RETRIES = 9
BACKOFF_FACTOR = 1 / MAX_REQUESTS_PER_SECOND