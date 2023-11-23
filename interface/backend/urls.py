from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from backend.api.views import TaskViewSet

router = routers.DefaultRouter()
router.register(r"tasks", TaskViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]
