from rest_framework.serializers import ModelSerializer

from shifokor.models import Shifokorlar


class ShifokorModelSerializer(ModelSerializer):
    class Meta:
        model = Shifokorlar
        fields = 'all'


