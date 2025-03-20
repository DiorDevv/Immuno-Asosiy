from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from shifokor.models import Shifokorlar, ShifokorQoshish
from .serializers import ShifokorModelSerializer, ShifokorListSerializer, ShifokorDetailUpdateModelSerializer
from shifokor.serializers import ShifokorQoshishModelSerializer
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.permissions import AllowAny


class ShifokorModelViewSet(ModelViewSet):
    queryset = Shifokorlar.objects.all()
    serializer_class = ShifokorModelSerializer
    permission_classes = (AllowAny,)

    def list(self, request, *args, **kwargs):
        self.serializer_class = ShifokorListSerializer
        return super().list(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.serializer_class = ShifokorDetailUpdateModelSerializer
        return super().update(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = ShifokorDetailUpdateModelSerializer
        return super().retrieve(request, *args, **kwargs)


class Shifokor_qoshish(CreateAPIView):
    queryset = ShifokorQoshish
    serializer_class = ShifokorQoshishModelSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            shifokor = self.queryset.objects.get(jshshir=request.data.get('jshshir'))
            return Response(
            {
                    "shifokor": {
                        "jshshir": shifokor.jshshir,
                        "ism": shifokor.ismi,
                        "familiya": shifokor.familya,
                        "tugilgan_sana": shifokor.tugilgan_sana,
                        "jinsi": shifokor.jinsi,
                    }
                },
                status=HTTP_200_OK
            )

        return Response(
            {
                "message": "Xatolik yuz berdi!",
                "errors": serializer.errors
            },
            status=HTTP_400_BAD_REQUEST
        )


