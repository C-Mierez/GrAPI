from rest_framework import serializers
from .models import User, Role
from django.contrib.auth.hashers import make_password

from rest_framework.exceptions import ValidationError
from GrAPI.mixins import ReadOnlyErrorMixin, UnexpectedParametersErrorMixin


class UserSerializer(ReadOnlyErrorMixin, UnexpectedParametersErrorMixin, serializers.HyperlinkedModelSerializer):
    # password = serializers.CharField(
    #     required=True,
    # )    
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), required=True)
    created_by = serializers.SlugRelatedField(read_only=True, slug_field='username')

    
    class Meta:
        model = User
        fields = ['url', 'username', 'password', 'role', 'is_active', 'date_joined', 'created_by']
        extra_kwargs = {
            'url': {
                'view_name': "user-detail"
            },
            'password': {
                'write_only': True,
                'required': True,
            },
            'date_joined': {
                'read_only': True
            },
            'is_active': {
                'read_only': True,
            },
        }
    
    def create(self, validated_data):
        # try:
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)
        # except ValueError as e:
        #     s = str(e)
        #     errorDesc = "Parameter Error: {desc}".format(desc=s)
        #     raise ValidationError(
        #         code='parameter_error',
        #         detail={
        #                 'parameter_error': (
        #                     errorDesc
        #                 )
        #             }
        #         )
        
    def update(self, instance, validated_data):
        return super(UserSerializer, self).update(instance, validated_data)
    
    def validate_role(self, value):
        if value.id == Role.ADMIN:
            raise ValidationError("Usuario debe tener un rol no administrador")        
        return value
    
    
    # def create(self, validated_data):
    #     groups_data = validated_data.pop('groups')
    #     user = User.objects.create(**validated_data)
    #     for group_data in groups_data:
    #         user.groups.add(group_data)
    #     return user