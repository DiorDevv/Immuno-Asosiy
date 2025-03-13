from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from shifokor.models import Shifokorlar, Shifokor_qoshish
from .serializers import ShifokorModelSerializer
from shifokor.serializers import Shifokor_qoshishModelSerializer
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.permissions import AllowAny


class ShifokorModelViewSet(ModelViewSet):
    queryset = Shifokorlar.objects.all()
    serializer_class = ShifokorModelSerializer
    permission_classes = (AllowAny,)


class Shifokor_qoshish(CreateAPIView):
    queryset = Shifokor_qoshish
    serializer_class = Shifokor_qoshishModelSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            data = self.queryset.filter(jshshir=request.data.get('jshshir'))

            return Response(
            {
                    "data": {
                        "JSHSHIR": data.JSHSHIR,
                        "ism": data.ism,
                        "familiya": data.familiya,
                        "tugilgan_sana": data.tugilgan_sana,
                        "jinsi": data.jinsi,
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


