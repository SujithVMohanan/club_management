from rest_framework import serializers
from apps.users.models import Users


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'username', 'name', 'home_name', 'is_active', 'is_staff', 'is_superuser', 'is_admin']

    
        
    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas
