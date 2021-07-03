from rest_framework import viewsets
from apps.schedule.models import Schedule
from apps.schedule.serializers import ScheduleSerializer
import datetime

# Create your views here.
class ScheduleViewSet(viewsets.ModelViewSet):
    serializer_class = ScheduleSerializer
    queryset = Schedule.objects.all()
    permission_classes = []
    
    def get_queryset(self):
        return self.queryset.filter(stream_date__gte=datetime.date.today())
