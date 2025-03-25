from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import CreateUserView, LoginAPIView #LoginRefreshView

urlpatterns = [
    path("signup/", CreateUserView.as_view(), name="signup"),
    path("login/", LoginAPIView.as_view(), name="login"),
    # path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('login/refresh/', LoginRefreshView.as_view(), name='login_refresh'),

]
