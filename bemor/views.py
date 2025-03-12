from rest_framework import status, generics, serializers
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from .models import BemorQoshish, Manzil, OperatsiyaBolganJoy, BemorningHolati, Bemor
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import BemorQoshishSerializer, ManzilSerializer, OperatsiyaBolganJoySerializer, \
    BemorningHolatiSerializer, BemorSerializer
from rest_framework import viewsets, permissions

from rest_framework import viewsets, filters


class BemorQoshishCreateView(CreateAPIView):
    queryset = BemorQoshish.objects.all()
    serializer_class = BemorQoshishSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            bemor_data = serializer.validated_data

            bemor, created = BemorQoshish.objects.get_or_create(
                JSHSHIR=bemor_data["JSHSHIR"],
                defaults=bemor_data
            )

            return Response(
                {
                    "message": "Bemor muvaffaqiyatli qo‘shildi!" if created else "Bemor allaqachon mavjud!",
                    "data": {
                        "JSHSHIR": bemor.JSHSHIR,
                        "ism": bemor.ism,
                        "familiya": bemor.familiya,
                        "tugilgan_sana": bemor.tugilgan_sana,
                        "jinsi": bemor.jinsi,
                    }
                },
                status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
            )

        return Response(
            {
                "message": "Xatolik yuz berdi!",
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class ManzilViewSet(viewsets.ModelViewSet):
    queryset = Manzil.objects.all()
    serializer_class = ManzilSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Faqat kirgan user POST, PUT, DELETE qila oladi


class OperatsiyaBolganJoyViewSet(viewsets.ModelViewSet):
    queryset = OperatsiyaBolganJoy.objects.all()
    serializer_class = OperatsiyaBolganJoySerializer

    def perform_create(self, serializer):
        # Qo‘shimcha tekshiruv: operatsiya sanasi tugash sanasidan oldin bo‘lishi kerak
        transplantatsiya_sana = serializer.validated_data.get('transplantatsiya_sana')
        operatsiya_oxirlangan_sana = serializer.validated_data.get('operatsiya_oxirlangan_sana')

        if transplantatsiya_sana > operatsiya_oxirlangan_sana:
            raise serializers.ValidationError(
                "Transplantatsiya sanasi operatsiya tugash sanasidan oldin bo‘lishi kerak!")

        serializer.save()


class BemorningHolatiViewSet(viewsets.ModelViewSet):
    queryset = BemorningHolati.objects.all()
    serializer_class = BemorningHolatiSerializer


class BemorViewSet(viewsets.ModelViewSet):
    """ Bemorlar uchun API """
    queryset = Bemor.objects.all().order_by('-created_at')  # Yangi bemorlar birinchi chiqadi
    serializer_class = BemorSerializer
    permission_classes = [IsAuthenticated]  # Faqat autentifikatsiya qilingan foydalanuvchilar foydalanishi mumkin
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['bemor__ism', 'bemor__familiya', 'bemor__JSHSHIR']  # Ism, familiya va JSHSHIR bo‘yicha qidirish
    ordering_fields = ['created_at', 'arxivga_olingan_sana']  # Saralash uchun maydonlar

    def perform_create(self, serializer):
        """ Yangi bemorni yaratishda avtomatik tekshirish va sozlash """
        serializer.save()

    def perform_update(self, serializer):
        """ Bemorni yangilashda validatsiyalarni qo‘shish """
        instance = serializer.instance
        if instance.arxivga_olingan_sana and instance.arxivga_olingan_sana < instance.created_at:
            raise serializers.ValidationError({"arxivga_olingan_sana": "Arxivga olish sanasi noto‘g‘ri!"})

        serializer.save()

    def perform_destroy(self, instance):
        """ Bemorni o‘chirish logikasi """
        if instance.arxivga_olingan_sana:
            raise serializers.ValidationError({"detail": "Arxivga olingan bemor o‘chirib bo‘lmaydi!"})
        instance.delete()
