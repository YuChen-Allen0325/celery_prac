from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'images', views.ImageViewSet)

urlpatterns = [
    path('task/', views.AddView.as_view(), name='task'),
    path('cache/', views.MyDataView.as_view(), name='cache'),
    path('', include(router.urls)),
]
