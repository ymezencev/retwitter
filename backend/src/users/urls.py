from django.conf.urls import url
from django.urls import include
from rest_framework.routers import DefaultRouter

from users import views

router = DefaultRouter()
# router.register(r'users', views.UserViewSet)
urlpatterns = [
    url(r'^auth/', include('rest_auth.urls')),
    url(r'^auth/registration/', include('rest_auth.registration.urls')),
]

urlpatterns += router.urls
