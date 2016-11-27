import json
import logging

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from . import models
from .livesession import iterate
from .find_path import find_shortest_path
from .models import MapLayer, Office, Scooter, Route, Station
from .serializers import MapLayerSerializer, OfficeSerializer, RouteSerializer, ScooterSerializer, StationSerializer


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
    user_id = request.GET.get('user_id')
    if user_id:
        routes = Route.objects.filter(user_id=user_id)
        routes.delete()
    floor_from = request.GET.get('floor_from')
    floor_to = request.GET.get('floor_to')
    x_from = request.GET.get('x_from')
    y_from = request.GET.get('y_from')
    x_to = request.GET.get('x_to')
    y_to = request.GET.get('y_to')
    if not floor_from or not floor_to or not x_from or not y_from or not x_to or not y_to:
        return Response(status=status.HTTP_404_NOT_FOUND)
    path = find_shortest_path(int(floor_from), (float(y_from), float(x_from)),
                                       int(floor_to), (float(y_to), float(x_to)))
    #logging.error()
    data = { 'path': json.dumps(path), 'user_id': user_id, 'status': models.ROUTE_STATUS_WAIT}
    serializer = RouteSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(path, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_route(request):
    user_id = request.POST.get('user_id', '')
    if not user_id:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    routes = Route.objects.filter(user_id=user_id, status=models.ROUTE_STATUS_WAIT)
    if len(routes.values()) == 0:
        return Response("Root not founds", status=status.HTTP_404_NOT_FOUND)
    scooters = Scooter.objects.filter(status__in=[models.SCOOTER_STATUS_FREE],
                                      floor=json.loads(routes.values()[0]['path'])[0][0])

    if len(scooters.values()) == 0:
        return Response("All resources are busy", status=status.HTTP_405_METHOD_NOT_ALLOWED)
    else:
        sc = Scooter.objects.get(id=scooters.values()[0]['id'])
        route = routes.values()[0]
        sc.route_id = route['id']
        route['status'] = models.ROUTE_STATUS_RUNNING
        sc.status = models.SCOOTER_STATUS_BUSY
        sc.save()
        rt = Route.objects.filter(id=route['id'])
        rt.update_or_create(route)
        #routes.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def iterate_step(request):
    scooters = Scooter.objects.filter(status=models.SCOOTER_STATUS_BUSY)
    for scooter in scooters.values():
        route = Route.objects.get(id=scooter['route_id'])
        path = json.loads(route.path)
        speed = 0.0005
        tick = 1
        new_pose, new_floor, new_path = iterate([scooter['y_coord'], scooter['x_coord']], scooter['floor'], path, speed, tick)
        if len(new_path) == 0:
            scooter['status'] = models.SCOOTER_STATUS_RETURNING
            station = Station.objects.get(id=scooter['home_station_id'])
            logging.error(station.y_coord)
            path = find_shortest_path(scooter['floor'], [scooter['y_coord'], scooter['x_coord']],
                                      station.floor, [station.y_coord, station.x_coord])

            path_serializer = RouteSerializer(data={'path': json.dumps(path), 'user_id': 1, 'status': models.ROUTE_STATUS_RUNNING})
            if path_serializer.is_valid():
                inst = path_serializer.save()
                scooter['route_id'] = inst.id
            else:
                logging.error(path_serializer.errors)
            route.delete()
        else:
            route.path = json.dumps(new_path)
            route.status = models.ROUTE_STATUS_RUNNING
            route.save()

        scooter['y_coord'] = new_pose[0]
        scooter['x_coord'] = new_pose[1]
        scooter['floor'] = new_floor

        sc = Scooter.objects.filter(id=scooter['id'])
        sc.update_or_create(scooter)
    scooters.update()
    scooters = Scooter.objects.filter(status=models.SCOOTER_STATUS_RETURNING)
    for scooter in scooters.values():
        route = Route.objects.get(id=scooter['route_id'])
        path = json.loads(route.path)
        speed = 0.0005
        tick = 1
        new_pose, new_floor, new_path = iterate([scooter['y_coord'], scooter['x_coord']], scooter['floor'], path, speed, tick)
        if len(new_path) == 0:
            scooter['status'] = models.SCOOTER_STATUS_FREE
            scooter['route_id'] = None
            route.delete()
        else:
            route.path = json.dumps(new_path)
            route.save()

        scooter['y_coord'] = new_pose[0]
        scooter['x_coord'] = new_pose[1]
        scooter['floor'] = new_floor

        sc = Scooter.objects.filter(id=scooter['id'])
        sc.update_or_create(scooter)
    scooters.update()
    return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
def scooters_data(request):
    scooters = Scooter.objects.all()
    serializer = ScooterSerializer(scooters, many=True)
    data = serializer.data
    for scooter in data:
        if scooter['route']:
            scooter['route'] = RouteSerializer(Route.objects.get(id=scooter['route'])).data
    return Response(data, status=status.HTTP_200_OK)

@api_view(['POST'])
def add_scooters(request):
    data = request.POST.copy()
    serializer = ScooterSerializer(data=data)
    if serializer.is_valid():
        serializer.save(home_station=Station.objects.get(floor=data['floor']))
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def station(request):
    if request.method == 'GET':
        stations = Station.objects.all()
        serializer = StationSerializer(stations, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = StationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)