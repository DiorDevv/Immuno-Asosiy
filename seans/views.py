from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from .models import Korik
from .serializers import KorikModelSerializer


class KorikModelViewSet(ModelViewSet):
    queryset = Korik.objects.all()
    serializer_class = KorikModelSerializer
