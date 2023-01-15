# youtube_query_monitor

## Local Setup

### Clone Repo

```shell
git clone https://github.com/sampan-s-nayak/youtube_query_monitor.git
cd youtube_query_monitor
```

### Providing server configurations:
Configurations are proided by adding into a `.env` file in project root dir, this is done to prevent creds from being stored in public repositories

.env variables to be specified:
```python
YOUTUBE_DATA_API_KEYS=google api key, pass a CSV when providing multiple keys
REFRESH_DURATION=video list refresh duration in seconds, ex: 10
SEARCH_QUERY=query to monitor, ex: cricket
MAX_PAGES_TO_QUERY=max number of youtube api pages to query, use a smaller number to prevent exceeding quota, ex: 100
DB_UPDATE_PARALLELISM=number of threads to spawn when updating entries in db, ideal setting depends on compute env, ex: 4
DEFAULT_PAGE_LIMIT=number of items per page in youtube_query_monitor api response, default is 25
# postgress db defaults
POSTGRES_DB=query_monitor
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
```

### Run Using Docker-Compose (Recommended)
once inside `youtube_query_monitor`, run 

```shell
docker-compose up --build
```

### Building Locally

```shell
python -m venv .venv 
. .venv/bin/activate
pip install -r requirements.txt
```

install and run redis, update `CELERY_BROKER_URL` and  `CELERY_RESULT_BACKEND` in `youtube_query_monitor/settings.py`

setup a postgress instance or switch to sqlite in settings.py file

```shell
# apply migrations
python manage.py migrate

# start server in terminal 1:
python manage.py runserver

# start celery worker in terminal 2:
celery -A youtube_query_monitor worker

# start celery django beat scheduler in terminal 3:
celery -A youtube_query_monitor beat -l info
```

## Test API

*Note:* use port 8000 if building locally,

```
# default settings:
curl http://localhost:82/videos/

# custom pagination
curl http://localhost:82/videos/\?limit\=10\&offset\=0

# filtering further on single word queries (case insensitive) (limit and offset is optional but will work as in previous case)
curl http://localhost:82/videos/\?limit\=10\&offset\=0\&query\=india

# filtering on multiword queries
curl http://localhost:82/videos/\?limit\=10\&offset\=0\&query\=inDia+virAt
```

## Future Enhancements:

- calling `get_video_list` utility api at server startup to prefill the db
- grafana prometheus setup for alerting and monitoring the service
- using Apache Solr as an alternative to postgres (Redis can also be explored as an option depending on usecae)
- moving to a compiled language from python
