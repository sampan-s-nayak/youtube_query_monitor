import os
from datetime import datetime, timedelta

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "youtube_query_monitor.settings")
app = Celery("youtube_query_monitor")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.task(bind=True)
def update_db(self):
    """
    We fetch the latest data from youtube API and add it to your DB.
    """
    from youtube_query_monitor.settings import RESULT_REFRESH_SECONDS, SEARCH_QUERY, DB_UPDATE_PARALLELISM
    from core.youtube_api_utils import get_video_list
    from concurrent.futures import ThreadPoolExecutor

    print("fetching videos...")
    published_after = (datetime.now() - timedelta(seconds=RESULT_REFRESH_SECONDS)).isoformat() + "Z"
    response = get_video_list(SEARCH_QUERY, published_after)
    print(f"fetched {len(response)} videos, saving to db....")

    workers = DB_UPDATE_PARALLELISM
    with ThreadPoolExecutor(workers) as pool:
        pool.map(_save_videos_in_db, response)


def _save_videos_in_db(video_item: dict):
    from core.models import Videos
    if not Videos.objects.filter(video_id=video_item["id"]["videoId"]).exists():
        snippet = video_item["snippet"]
        video = Videos(
            video_id=video_item["id"]["videoId"],
            video_title=snippet["title"],
            description=snippet["description"],
            published_on=snippet["publishedAt"],
            thumb_url=snippet["thumbnails"]["default"]["url"],
            link="https://www.youtube.com/watch?v=" + video_item["id"]["videoId"],
        )
        video.save()
