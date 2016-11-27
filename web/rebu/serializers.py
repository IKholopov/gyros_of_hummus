from rest_framework import serializers

from .models import MapLayer, Office, Route, Scooter, Station


class MapLayerSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=True, allow_blank=False, max_length=128)
    field = serializers.CharField(required=True, allow_blank=False)
    floor = serializers.IntegerField(required=True)
    a_align_x = serializers.FloatField(required=False, allow_null=True)
    a_align_y = serializers.FloatField(required=False, allow_null=True)
    b_align_x = serializers.FloatField(required=False, allow_null=True)
    b_align_y = serializers.FloatField(required=False, allow_null=True)

    def create(self, validated_data):
        return MapLayer.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.field = validated_data.get('field', instance.field)
        instance.floor = validated_data.get('floor', instance.floor)
        instance.a_align_x = validated_data.get('a_align_x', instance.a_align_x)
        instance.a_align_y = validated_data.get('a_align_y', instance.a_align_y)
        instance.b_align_x = validated_data.get('b_align_x', instance.b_align_x)
        instance.b_align_y = validated_data.get('b_align_y', instance.b_align_y)

class RouteSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    path = serializers.CharField(required=True)
    user_id = serializers.IntegerField(allow_null=True)
    status = serializers.IntegerField(allow_null=True)

    def create(selfself, validated_data):
        return Route.objects.create(**validated_data)

class ScooterSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    x_coord = serializers.FloatField(required=True)
    y_coord = serializers.FloatField(required=True)
    speed = serializers.FloatField(required=True)
    floor = serializers.FloatField(required=True)
    status = serializers.IntegerField(required=True)
    route = serializers.PrimaryKeyRelatedField(read_only=True)
    home_station = serializers.PrimaryKeyRelatedField(read_only=True)

    def create(self, validated_data):
        return Scooter.objects.create(**validated_data)

class StationSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    x_coord = serializers.FloatField(required=True)
    y_coord = serializers.FloatField(required=True)
    floor = serializers.FloatField(required=True)

    def create(self, validated_data):
        return Station.objects.create(**validated_data)


class OfficeSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True)
    floor = serializers.IntegerField(required=True)
    x_coord = serializers.IntegerField(required=True)
    y_coord = serializers.IntegerField(required=True)

    def create(self, validated_data):
        return Office.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.floor = validated_data.get('floor', instance.floor)
        instance.x_coord= validated_data.get('x_coord', instance.x_coord)
        instance.y_coord = validated_data.get('y_coord', instance.y_coord)