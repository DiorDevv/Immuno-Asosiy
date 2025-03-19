from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from seans.models import Korik
from seans.serializers import KorikModelSerializer


class KorikModelViewSet(ModelViewSet):
    queryset = Korik.objects.all()
    serializer_class = KorikModelSerializer
