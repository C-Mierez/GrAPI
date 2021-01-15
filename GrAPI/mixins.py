from rest_framework.exceptions import ValidationError
from rest_framework.fields import empty
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