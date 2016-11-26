import json
import logging

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from . import models
from .livesession import iterate
from .find_path import find_shortest_path
from .models import MapLayer, Office, Scooter, Route
from .serializers import MapLayerSerializer, OfficeSerializer, RouteSerializer


def editor(request):
    return render(request, 'editor.html')

@api_view(['GET', 'POST'])
def office_list(request):
    if request.method == 'GET':
        offices = Office.objects.all()
        serializer = OfficeSerializer(offices, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = OfficeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE'])
def office(request, name):
    try:
        office = Office.objects.get(name=name)
    except Office.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = OfficeSerializer(office)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'DELETE':
        office.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def map_layer_list(request):
    if request.method == 'GET':
        layers = MapLayer.objects.all()
        serializer = MapLayerSerializer(layers, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = MapLayerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def map_layer(request, floor):
    try:
        layer = MapLayer.objects.get(floor=floor)
    except MapLayer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MapLayerSerializer(layer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = MapLayerSerializer(layer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        layer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def navigate(request):
    floor_from = request.GET.get('floor_from')
    floor_to = request.GET.get('floor_to')
    x_from = request.GET.get('x_from')
    y_from = request.GET.get('y_from')
    x_to = request.GET.get('x_to')
    y_to = request.GET.get('y_to')
    if not floor_from or not floor_to or not x_from or not y_from or not x_to or not y_to:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(find_shortest_path(int(floor_from), (float(y_from), float(x_from)),
                                       int(floor_to), (float(y_to), float(x_to))), status=status.HTTP_200_OK)

@api_view(['POST'])
def create_route(request):
    logging.error(request.POST)
    route = request.POST.get('path', '')
    if not route:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    scooters = Scooter.objects.filter(status__in = [models.SCOOTER_STATUS_FREE, models.SCOOTER_STATUS_RETURNING])
    if len(scooters.values()) == 0:
        return Response("All resources are busy", status=status.HTTP_408_REQUEST_TIMEOUT)
    serializer = RouteSerializer(data=request.data)
    if serializer.is_valid():
        instance = serializer.save()
        logging.error(instance)
        sc = Scooter.objects.get(id=scooters.values()[0]['id'])
        sc.route_id = instance.id
        sc.status = models.SCOOTER_STATUS_BUSY
        sc.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def iterate_step(request):
    scooters = Scooter.objects.filter(status=models.SCOOTER_STATUS_BUSY)
    for scooter in scooters.values():
        route = Route.objects.get(id=scooter['route_id'])
        path = json.loads(route.path)
        speed = 0.2
        tick = 3
        new_pose, new_path = iterate([scooter['x_coord'], scooter['y_coord']], path, speed, tick)
        if len(new_path) == 0:
            scooter['status'] = models.SCOOTER_STATUS_FREE
            route.delete()
        else:
            route.path = json.dumps(new_path)
            route.save()

        scooter['x_coord'] = new_pose[0]
        scooter['y_coord'] = new_pose[1]
        logging.error(scooters.values())
        Scooter.objects.update_or_create(scooter)
    scooters.update()
    return Response(status=status.HTTP_200_OK)