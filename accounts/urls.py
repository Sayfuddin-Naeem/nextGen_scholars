from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StudentViewSet,
    TeacherViewSet,
    UserLoginApiView,
    UserLogoutApiView,
    PasswordUpdateApiView,
    activate
)

router = DefaultRouter()
router.register('teacher', TeacherViewSet, basename='teacher')
router.register('student', StudentViewSet, basename='student')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('login/', UserLoginApiView.as_view(), name='login'),
    path('logout/', UserLogoutApiView.as_view(), name='logout'),
    path('password/change/', PasswordUpdateApiView.as_view(), name='change_password'),
    path('activate/<uid64>/<token>/', activate, name='activate'),
]