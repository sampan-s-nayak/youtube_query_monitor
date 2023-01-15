from django.core import serializers
from django.http import HttpResponse
from rest_framework.decorators import api_view
from core.models import Videos
from django.db.models import Q

from youtube_query_monitor.settings import DEFAULT_PAGE_LIMIT


# Create your views here.
@api_view(['GET'])
def get_videos(request):
    """
    Query Params:
    -limit (optional): INT -> number of videos to be returned per page (DEFAULT: configurable)
    -offset (optional): INT -> page/item offset (DEFAULT: 0)
    -query (Optional): STR -> query term to filter on the list of videos further (case insensitive) (DEFAULT: None)

    :return: list of videos (json string)
    """
    limit = int(request.GET.get('limit', DEFAULT_PAGE_LIMIT))
    offset = int(request.GET.get('offset', 0))
    query = request.GET.get('query')

    if query:
        query = query.strip()
        tokens = query.split()

        query_filter = None
        for i in range(len(tokens)):
            if i == 0:
                query_filter = (Q(video_title__icontains=tokens[0]) | Q(description__icontains=tokens[0]))
            else:
                query_filter = query_filter & (
                            Q(video_title__icontains=tokens[i]) | Q(description__icontains=tokens[i]))

        paginated_response = Videos.objects.filter(
            query_filter
        ).order_by('-published_on')[offset:offset + limit]

    else:
        paginated_response = Videos.objects.order_by('-published_on')[offset:offset + limit]

    return HttpResponse(serializers.serialize('json', paginated_response), content_type='application/json')
