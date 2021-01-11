from django.db import models, transaction
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, BaseUserManager, Group)
from django.utils import timezone
from GrAPI.models import SoftDeletionUserModel, SoftDeletionUserManager
import uuid

class Role(models.Model):
    # Constantes
    ADMIN = 1
    GUARD = 2
    
    # Tuplas para elegir
    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (GUARD, 'Guard'),
    )
    
    id      = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)
    
    def __str__(self):
      return self.get_id_display()
    

class UserManager(SoftDeletionUserManager):
    
    def create_user(self, username, role, password=None, **kwargs):
        if not username:
            raise ValueError('Usuario debe tener un username')
        # if not kwargs["group_id"]:
        #     raise ValueError('Usuario debe ser parte de un grupo')
        
        try:
            with transaction.atomic():
                user = self.model(username= username, role_id=role, **kwargs)
                # group = Group.objects.get(pk=kwargs["group_id"])
                # group.user_set.add(user)
                user.set_password(password)
                user.save(using= self._db)
        except:
            raise
        return user
    
    def create_superuser(self, username, role=Role.ADMIN, password=None):
        user = self.create_user(username, role, password=password)
        
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        
        return user

class User(SoftDeletionUserModel, PermissionsMixin):
    """ Modelo para representar al usuario """
    id          = models.AutoField(primary_key=True)
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username    = models.CharField(max_length=127, unique=True)
    is_active   = models.BooleanField(default=True)
    is_staff    = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    role        = models.ForeignKey(Role, on_delete=models.PROTECT, default=2)
    
    #? "SoftDeletionUserModel" define un manager como 'objects'. 
    #? UserManager extiende de SoftDeletionUserManager
    objects = UserManager()
    
    #? Además, se define 'all_objects' para ver todos los usuarios
    
    
    # Se define el atributo a ser considerado como Unique por el backend
    # de Django
    USERNAME_FIELD = 'username'
    
    # Campos obligatorios al crear un superuser
    # EJEMPLO: REQUIRED_FIELDS = ['name']
    REQUIRED_FIELDS = ['role']
    
    def get_full_name(self):
        return self.username
    
    def __str__(self):
        return self.username
    
