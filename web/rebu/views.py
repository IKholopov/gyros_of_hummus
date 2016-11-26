import logging

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from .find_path import find_shortest_path
from .models import MapLayer, Office
from .serializers import MapLayerSerializer, OfficeSerializer


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
