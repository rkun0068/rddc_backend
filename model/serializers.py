import json

from rest_framework import serializers
from .models import DetectionResult


class DetectionResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = DetectionResult
        fields = ['img_url', 'result', 'created']

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation["result"] = json.loads(instance.result)
    #     return representation
