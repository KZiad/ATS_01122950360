from django.shortcuts import render

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from apps.events.models import Event
from apps.accounts.models import User
from apps.events.serializers import EventSerializer
from rest_framework import serializers

class BookingSerializer(serializers.Serializer):
    # Add fields if you want to accept data in POST, or leave empty for your use-case
    pass

class BookingCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated,]
    queryset = Event.objects.all()
    serializer_class = BookingSerializer
    def post(self, request, *args, **kwargs):
        event_id = kwargs.get('pk')
        event = Event.objects.get(id=event_id)
        user = request.user
        

        if user in event.booked_by.all():
            return Response({"message": "You have already booked this event."}, status=status.HTTP_400_BAD_REQUEST)

        event.booked_by.add(user)
        event.save()

        return Response({"message": "Event booked successfully."}, status=status.HTTP_201_CREATED)
