from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from quickstart.serializers import UserSerializer, GroupSerializer, CurrenciesSerializer
from quickstart.models import Currencies
import requests
import json
from datetime import datetime, timedelta

from quickstart.exchange import CurrencyClass


open_exchange_rates_id = '###'
open_exchange_rates_api_location = "https://openexchangerates.org/api/latest.json?app_id="
request_address = open_exchange_rates_api_location + open_exchange_rates_id
rates_file = 'rates.json'
file = rates_file
currencies_list = ['USD', 'EUR', 'CZK', 'PLN']



class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def curr_list(request):
    """
    List all currences rates
    """
    if request.method == 'GET':
        all_rates = Currencies.objects.all()
        serializer = CurrenciesSerializer(all_rates, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def update_rates(request):
    """
    Update currency rates from remote source
    """
    if request.method == 'GET':
        obj = requests.get(request_address).json()
        curr_inst = Currencies()
        curr_inst.timestamp = obj['timestamp']
        curr_inst.usd = obj['rates']['USD']
        curr_inst.eur = obj['rates']['EUR']
        curr_inst.czk = obj['rates']['CZK']
        curr_inst.pln = obj['rates']['PLN']
        curr_inst.save()
        serializer = CurrenciesSerializer(curr_inst)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def convert(request, fromto, amount):
    latests_rates = Currencies.objects.all().order_by('-id')[0]
    serializer = CurrenciesSerializer(latests_rates)
    from_curr = fromto[0:3].upper()
    to_curr = fromto[3:6].upper()
    if from_curr not in currencies_list or to_curr not in currencies_list:
        return Response(
            {'result': 'incorrect currencies'},
            status=status.HTTP_400_BAD_REQUEST
        )

    dummy_object = CurrencyClass(rates_file, request_address)
    result = dummy_object.curr_to_curr(from_curr, to_curr, amount)


    return Response(
        {'from_curr': from_curr,
         'to_curr': to_curr,
         'amount': amount,
         'result': result
         })

