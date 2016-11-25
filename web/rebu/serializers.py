from rest_framework import serializers

from .models import MapLayer


class MapLayerSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=True, allow_blank=False, max_length=128)
    field = serializers.CharField(required=True, allow_blank=False)
    floor = serializers.IntegerField(required=True)
    a_align_x = serializers.FloatField(required=True)
    a_align_y = serializers.FloatField(required=True)
    b_align_x = serializers.FloatField(required=True)
    b_align_y = serializers.FloatField(required=True)

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
