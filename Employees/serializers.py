from rest_framework import serializers
from .models import EmployeeManager, Employee

from rest_framework.fields import empty
from rest_framework.exceptions import ValidationError
from rest_framework.settings import api_settings

class ReadOnlyErrorMixin:
    def run_validation(self, data=empty):
        for fieldname, field in self.fields.items():
            if field.read_only and fieldname in data.keys():
                raise ValidationError(
                    code='write_on_read_only_field',
                    detail={
                        fieldname: (
                            f"You're trying to write to the field "
                            "'{fieldname}' which is a read-only field."
                        )
                    }
                )
        return super().run_validation(data)
    
class UnexpectedParametersErrorMixin:
    def run_validation(self, data=empty):
        if data is not empty:
            unknown = set(data) - set(self.fields)
            if unknown:
                errors = ["Unknown field: {}".format(f) for f in unknown]
                raise ValidationError({
                    api_settings.NON_FIELD_ERRORS_KEY: errors,
                })
        return super().run_validation(data)
    

class EmployeeSerializer(ReadOnlyErrorMixin, serializers.HyperlinkedModelSerializer):   
    
    user = serializers.HyperlinkedRelatedField(read_only=True, view_name='user-detail')
    role = serializers.SerializerMethodField()
    
    def get_role(self, obj):
        try:
            role = obj.user.role.id
            return role
        except:
            return None
    
    class Meta:
        model = Employee
        fields = ['url', 'name', 'surname', 'employee_id', 'user', 'role', 'id']
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
    
    