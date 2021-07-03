from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from apps.schedule.views import ScheduleViewSet

router = DefaultRouter()
router.register("schedule", ScheduleViewSet, basename="schedule")
schedule_urlpatterns = [url("api/v1/", include(router.urls))]
