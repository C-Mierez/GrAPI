from rest_framework import serializers
from .models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'is_staff',]
    
    # def create(self, validated_data):
    #     groups_data = validated_data.pop('groups')
    #     user = User.objects.create(**validated_data)
    #     for group_data in groups_data:
    #         user.groups.add(group_data)
    #     return user