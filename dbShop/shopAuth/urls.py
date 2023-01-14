from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import *


app_name = 'shopAuth'
urlpatterns = [
    path('registration/', RegistrationAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('user/', CustomUserRetrieveUpdateAPIView.as_view()),
    path('refresh/', RefreshView.as_view())
]

router = DefaultRouter()
router.register(r'jobs', JobViewSet, basename='job')
router.register(r'profiles', ProfileViewSet, basename='profile')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'working', WorkDayViewSet, basename='working')
router.register(r'dayoffs', DayOffViewSet, basename='dayoff')
router.register(r'vacations', VacationViewSet, basename='vacations')
urlpatterns += router.urls