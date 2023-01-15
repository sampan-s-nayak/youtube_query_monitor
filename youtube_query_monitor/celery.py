import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "youtube_query_monitor.settings")
app = Celery("youtube_query_monitor")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.task(bind=True)
def test_worker(self):
    print("Testing Worker!")


@app.task(bind=True)
def update_db(self):
    """
    We fetch the latest data from youtube API and add it to your DB.
    """
    from youtube_api.models import Videos
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError

    DEVELOPER_KEY = 'AIzaSyCh8vY27xrCzLrpXl32FpG5F1rjp_ksYSE'
    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = 'v3'

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    print("fetch videos")

    response = youtube.search().list(
        q="cricket",
        part='id,snippet',
        maxResults=30
    ).execute()

    for item in response.get("items", []):
        snippet = item["snippet"]
        try:
            video = Videos(
                video_id=item["id"]["videoId"],
                video_title=snippet["title"],
                description=snippet["description"],
                published_on=snippet["publishedAt"],
                thumb_url=snippet["thumbnails"]["default"]["url"],
                link="https://www.youtube.com/watch?v=" + item["id"]["videoId"],
            )
            video.save()
        except Exception as e:
            # update cases
            print(f"could not update video: {video}")
            pass
