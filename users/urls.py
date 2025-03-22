from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import UserViewSet

app_name = UsersConfig.name

router_user = SimpleRouter()
router_user.register('users', UserViewSet, basename='users')

urlpatterns = router_user.urls + [
    path('users/login', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='user_login'),
    path('users/token/refresh', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='user_token_refresh'),

]
