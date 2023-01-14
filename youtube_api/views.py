from django.core import serializers
from django.http import HttpResponse
from rest_framework.decorators import api_view
from youtube_api.models import Videos


# Create your views here.
@api_view(['GET'])
def index(request):
    limit = int(request.GET.get('limit'))
    offset = int(request.GET.get('offset'))
    paginated_response = Videos.objects.order_by('-published_on')[offset:offset + limit]
    return HttpResponse(serializers.serialize('json', paginated_response), content_type='application/json')
