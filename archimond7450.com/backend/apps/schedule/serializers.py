from rest_framework import serializers
from apps.schedule.models import Schedule

"""class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        read_only_fields = ((
            "id",
        ))
        fields = (
            "id",
            "stream_date",
            "start_time",
            "end_time",
            "what",
            "description",
        )
"""

class ScheduleSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    stream_date = serializers.DateField(format="%a, %d %b")
    start_time = serializers.TimeField(format="%H:%M")
    end_time = serializers.TimeField(format="%H:%M")
    what = serializers.CharField(max_length=24)
    description = serializers.CharField(max_length=128)
