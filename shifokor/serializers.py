from rest_framework.serializers import ModelSerializer

from .models import Shifokorlar


class ShifokorModelSerializer(ModelSerializer):
    class Meta:
        model = Shifokorlar
        fields = 'all'


print("ds")