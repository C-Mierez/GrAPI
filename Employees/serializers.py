from rest_framework import serializers
from .models import EmployeeManager, Employee

from rest_framework.exceptions import ValidationError
from GrAPI.mixins import ReadOnlyErrorMixin, UnexpectedParametersErrorMixin

class EmployeeSerializer(ReadOnlyErrorMixin, serializers.HyperlinkedModelSerializer):   
    
    user = serializers.HyperlinkedRelatedField(read_only=True, view_name='user-detail')
    role = serializers.SerializerMethodField(read_only=True)
    is_active = serializers.SerializerMethodField(read_only=True)
    
    def get_role(self, obj):
        try:
            role = obj.user.role.id
            return role
        except:
            return None
        
    def get_is_active(self, obj):
        try:
            is_active = obj.user.is_active
            return is_active
        except:
            return None
    
    class Meta:
        model = Employee
        fields = ['url', 'name', 'surname', 'employee_id', 'user', 'role', 'is_active', 'id']
        extra_kwargs = {
            'url': {
                'view_name': "employee-detail"
            },
            'name': {
                'required': True
            },
            'surname': {
                'required': True
            },
            'employee_id': {
                'required': True
            },
            'user': {
                'read_only': True
            },
            'id': {
                'read_only': True
            }
        }
    
    def create(self, validated_data):
        print(validated_data)
        return super(EmployeeSerializer, self).create(validated_data)
        
    def update(self, instance, validated_data):
        return super(EmployeeSerializer, self).update(instance, validated_data)
    
    