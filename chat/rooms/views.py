from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Room, Message
from .serializers import RoomSerializer

@login_required
def rooms(request):
    rooms = Room.objects.all()
    return render(request, 'rooms/rooms.html', {'rooms': rooms})

@login_required
def room(request, pk):
    room = Room.objects.get(pk=pk)
    messages = Message.objects.filter(room=room)[0:25]

    return render(request, 'rooms/room.html', {'room': room, 'messages': messages})

class RoomAPIView(APIView):
    def get(self, request):
        lst = Room.objects.all()
        return Response({'Rooms': RoomSerializer(lst, many=True).data})

    def post(self, request):
        serializer = RoomSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()    

        return Response({'Room': serializer.data})
    

    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method PUT not allowed"})

        try:
            instance = Room.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})

        serializer = RoomSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)   
        serializer.save()
        return Response({'Room': serializer.data})
    
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method DELETE not allowed"})
        else:
            instance = Room.objects.get(pk=pk)
            instance.delete()

        return Response({"Room": "delete post " + str(pk)})