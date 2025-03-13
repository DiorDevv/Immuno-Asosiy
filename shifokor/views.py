from rest_framework.viewsets import ModelViewSet

from shifokor.models import Shifokorlar
from serializers import ShifokorModelSerializer

class ShifokorModelViewSet(ModelViewSet):
    queryset = Shifokorlar.objects.all()
    serializer_class = ShifokorModelSerializer


