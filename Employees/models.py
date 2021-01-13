from django.db import models, transaction
from django.conf import settings
from Users.models import User, Role

def generate_username(last_name,employee_id):
    val = "{0}_{1}".format(last_name,employee_id).lower()
    x=0
    while True:
        if x == 0 and User.objects.filter(username=val).count() == 0:
            return val
        else:
            new_val = "{0}_{1}".format(val,x)
            if User.objects.filter(username=new_val).count() == 0:
                return new_val
        x += 1
        if x > 1000000:
            raise Exception("Failed to generate username.")
        

class EmployeeManager(models.Manager):
    def create(self, name, surname, employee_id, created_by, **kwargs):
        if not name:
            raise ValueError('Usuario debe tener el parametro  name')
        if not surname:
            raise ValueError('Usuario debe tener el parametro surname')
        if not employee_id:
            raise ValueError('Usuario debe tener el parametro  employee_id')
        if not created_by:
            raise ValueError('Usuario debe tener el parametro  created_by')
        try:
            role = Role.objects.get(pk=Role.GUARD)
        except Role.DoesNotExist:
            raise ValueError('Rol default del usuario no existe.')
        
        newUsername = generate_username(last_name=surname, employee_id=employee_id)
        newPassword = '12345'
        try:
            with transaction.atomic():
                user = User.objects.create(username=newUsername, role=role, created_by=created_by, password=newPassword)
                employee = self.model(name=name, surname=surname, employee_id=employee_id, user=user, **kwargs)
                employee.save(using= self._db)
                return employee
        except:
            raise
        return employee

class Employee(models.Model):
    id      = models.AutoField(primary_key=True)
    name    = models.CharField(max_length=127, blank=False, null=False)
    surname = models.CharField(max_length=127, blank=False, null=False)
    employee_id = models.CharField(max_length=127, blank=False, null=False)
    
    user    = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='user_of', on_delete=models.PROTECT, blank=True, null=True)
    
    objects = EmployeeManager()