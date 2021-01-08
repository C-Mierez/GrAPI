from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
    )
    
    role = serializers.PrimaryKeyRelatedField(read_only=True)

    
    class Meta:
        model = User
        fields = ['url', 'username', 'is_staff', 'password', 'role',]
    
    
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)
    
    # def create(self, validated_data):
    #     groups_data = validated_data.pop('groups')
    #     user = User.objects.create(**validated_data)
    #     for group_data in groups_data:
    #         user.groups.add(group_data)
    #     return user