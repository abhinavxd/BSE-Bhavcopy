from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.conf import settings
from datetime import datetime
import json
import redis

redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                  port=settings.REDIS_PORT, db=0)


def get_stock_data_for_dates(keys):
    """
    Get record for stock by dates

    Args:
        keys (list): List of dates for stock

    Returns:
        list: list of dicts with searched stock data per dict
    """
    all_values = []
    values = None
    for key in keys:
        if isinstance(key, bytes):
            key = key.decode('utf-8')
        date = key.split(':')[-1]
        # Get all fields for key (name:date) 
        values = redis_instance.hgetall(key)
        values = {k.decode('utf-8'): v.decode("utf-8") for k,v in values.items()}
        values = {'DATE': date, **values}
        all_values.append(values)
    return all_values

@api_view(['POST'])
def search_by_name(request):
    """
    Search stock by complete name

    Args:
        request Request: Request object

    Returns:
        dict: Dict with searched stock data
    """
    post_data = json.loads(request.body.decode('utf-8'))
    if 'sc_name' in post_data:
        stock_name = post_data['sc_name']

        # Get all available dates for this stock
        dates = redis_instance.smembers(f'{stock_name}')
        # sort the dates
        dates = sorted(dates, key=lambda date: datetime.strptime(date.decode('utf-8'), '%d-%m-%y'))

        # Generate keys for hmset
        keys = [f"{stock_name}:{date.decode('utf-8')}" for date in dates]
        values = get_stock_data_for_dates(keys)        
        return Response({"name": stock_name, "data": values}, status=200)
    else:
        return Response('Bad request', status=400)

@api_view(['POST'])
def search_prefix(request):
    """
    Return matching stock names to prefix

    Returns:
        list : List of dicts with matching stock prefixes e.g [{title: 'stockname1'}, {title: 'stockname2'}]
    """
    post_data = json.loads(request.body.decode('utf-8'))
    if 'search_term' in post_data:
        search_term = post_data['search_term']
        searched_names = redis_instance.smembers(f'{search_term.upper()}')
        stock_names = [{'title' : name.decode('utf-8')} for name in searched_names]
        return Response(stock_names, status=200)
    else:
        return Response('Bad request', status=400)
