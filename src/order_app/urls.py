from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()

router.register("", views.OrderViewSet, "order")
router.register("item", views.OrderItemViewSet, "order_item")

urlpatterns = [
    path('', include(router.urls))
]
