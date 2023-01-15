from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from youtube_query_monitor.settings import YOUTUBE_DATA_API_KEYS, SEARCH_QUERY, MAX_PAGES_TO_QUERY_FROM_YOUTUBE

DEVELOPER_KEYS = YOUTUBE_DATA_API_KEYS
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

YOUTUBE_CLIENTS = [build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                         developerKey=dev_key) for dev_key in DEVELOPER_KEYS.split(',')]

# Default API params
DEFAULT_MAX_RESPONSE_SIZE = 25
DEFAULT_ORDER_BY_FIELD = 'date'
DEFAULT_PARTS = 'id,snippet'


def get_video_list(query: str = SEARCH_QUERY, published_after: str = '1970-01-01T00:00:00Z'):
    items = []
    num_pages_queried = 1
    next_page_token = None

    for i, client in enumerate(YOUTUBE_CLIENTS):
        try:
            if not next_page_token:
                # fetching first page of the response
                response = client.search().list(
                    q=query,
                    part=DEFAULT_PARTS,
                    maxResults=DEFAULT_MAX_RESPONSE_SIZE,
                    order=DEFAULT_ORDER_BY_FIELD,
                    publishedAfter=published_after
                ).execute()
                items.extend(response.get("items"))
                next_page_token = response.get("nextPageToken")

            while next_page_token and num_pages_queried < MAX_PAGES_TO_QUERY_FROM_YOUTUBE:
                # fetching subsequent pages of the search api response
                response = client.search().list(
                    q=query,
                    part=DEFAULT_PARTS,
                    maxResults=DEFAULT_MAX_RESPONSE_SIZE,
                    order=DEFAULT_ORDER_BY_FIELD,
                    publishedAfter=published_after,
                    pageToken=next_page_token
                ).execute()
                items.extend(response.get("items"))
                next_page_token = response.get("nextPageToken")
                num_pages_queried += 1
            return items
        except HttpError as e:
            print(f"encountered error: {e}")
            if e.resp.status == 403:
                print(f"request failed using key {i+1}, trying with next key if available....")
    print("Run out of keys to try!")
    return []
