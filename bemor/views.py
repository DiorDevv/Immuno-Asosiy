from rest_framework import status, generics, serializers
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from .models import BemorQoshish, Manzil, OperatsiyaBolganJoy, BemorningHolati, Bemor, Viloyat, Tuman
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import BemorQoshishSerializer, ManzilSerializer, OperatsiyaBolganJoySerializer, \
    BemorningHolatiSerializer, BemorSerializer
from rest_framework import viewsets, permissions
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import viewsets, filters
from rest_framework.exceptions import ValidationError


class BemorQoshishCreateView(CreateAPIView):
    queryset = BemorQoshish.objects.all()
    serializer_class = BemorQoshishSerializer
    permission_classes = [AllowAny]

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


class BemorViewSet(viewsets.ModelViewSet):
    queryset = Bemor.objects.all().order_by('-created_at')
    serializer_class = BemorSerializer
    permission_classes = []
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['bemor__ism', 'bemor__familiya', 'bemor__JSHSHIR']
    ordering_fields = ['created_at', 'arxivga_olingan_sana']

    def create(self, request, *args, **kwargs):
        """Agar bemor allaqachon bazada bo‘lsa, yangi yaratmaydi, balki mavjud bemorni qaytaradi"""
        try:
            bemor_id = request.data.get("bemor")

            if not bemor_id:
                raise ValidationError({"error": "Bemor ID kiritilishi shart!"})

            # Bemor mavjudligini tekshirish
            if not Bemor.objects.filter(id=bemor_id).exists():
                return Response(
                    {"error": "Bunday bemor mavjud emas!"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Agar bemor allaqachon ro‘yxatda bo‘lsa, qaytaramiz
            existing_bemor = Bemor.objects.filter(bemor=bemor_id, manzil=request.data.get("manzil")).first()
            if existing_bemor:
                return Response(
                    {
                        "message": "Bu bemor allaqachon ro‘yxatda bor!",
                        "bemor": BemorSerializer(existing_bemor).data
                    },
                    status=status.HTTP_200_OK
                )

            return super().create(request, *args, **kwargs)

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Server xatosi: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
