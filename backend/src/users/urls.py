from django.conf.urls import url
from django.urls import include
from rest_framework.routers import DefaultRouter, SimpleRouter

from users import views

router = SimpleRouter()

# router.register(r'auth/user-info', views.UserPersonalInfoDetailView)
router.register(r'auth/user-info', views.UserPersonalInfoDetailView,
                'user-info')

urlpatterns = [
    url(r'^auth/', include('rest_auth.urls')),
    url(r'^auth/registration/', include('rest_auth.registration.urls')),
]

urlpatterns += router.urls
