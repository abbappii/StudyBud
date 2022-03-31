from rest_framework.decorators import api_view
from rest_framework.response import Response

from base.models import Rooms
from .serializers import RoomSerializers
from base.api import serializers

@api_view(['GET'])
def getRooms(request):

    rooms = Rooms.objects.all()
    serializer = RoomSerializers(rooms, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getRoom(request,pk):

    room = Rooms.objects.get(id=pk)
    serializer = RoomSerializers(room, many=False)
    return Response(serializer.data)