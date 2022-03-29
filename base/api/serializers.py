from ast import Mod
from  rest_framework.serializers import ModelSerializer
from  base.models import Rooms

class RoomSerializers(ModelSerializer):
    class Meta:
        model = Rooms
        fields = '__all__'

