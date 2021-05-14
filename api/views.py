from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.conf import settings
import json
import redis

redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                  port=settings.REDIS_PORT, db=0)

@api_view(['POST'])
def search_name(request):
    post_data = json.loads(request.body.decode('utf-8'))
    if 'sc_name' in post_data:
        search_term = post_data['sc_name'].upper()
        response = []
        for term in redis_instance.scan_iter(f"{search_term}*"):
            response.append(eval(redis_instance.get(term)))
        if len(response) > 0:
            return Response(response, status=200)
        else:
            return Response('Not found', status=404)
    else:
        return Response('Not found', status=404)
