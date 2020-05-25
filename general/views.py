from django.shortcuts import render
from users.models import Users
from vehicle_registration.models import Vehicles
# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
import json


# Create your views here.
@api_view(http_method_names=['GET'])
@renderer_classes((JSONRenderer,))
def participants(request):
    authority = Users.objects.filter(user_type=1).values()
    agent = Users.objects.filter(user_type=2).values()
    owner = Users.objects.filter(user_type=3).values()

    parts = {'peer1_Authority': authority,
             'peer2_Agent': agent,
             'peer3_Owner': owner
             }
    return Response(parts)


@api_view(http_method_names=['GET'])
@renderer_classes((JSONRenderer,))
def assets(request):
    asset = Vehicles.objects.all().values()
    return Response(asset)


@api_view(http_method_names=['GET'])
@renderer_classes((JSONRenderer,))
def ledger(request):
    ledgers = []
    ledge = {'assets': '/assets/',
             'participants': '/participants/',
             'transactions': '/transactions/'
             }
    ledgers.append(ledge)
    return Response(ledgers)
